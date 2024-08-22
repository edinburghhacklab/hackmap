#!/usr/bin/env python
import asyncio
import json
import os
import dataclasses
from dataclasses import dataclass
from datetime import datetime

from asyncio_paho import AsyncioPahoClient
from paho.mqtt.client import MQTTMessage
from websockets.asyncio.server import (
    broadcast,
    serve,
    ServerConnection as WebsocketConnection,
)
from hackmap.local_settings import (
    DEBUG,
    MQTT_HOST,
    ROOM_ACTIVE_TIME,
    ROOM_EXPIRY_POLL_SECS,
    WEBSOCKET_BIND,
)

ROOM_WHITELIST = ["g1", "g2", "g8", "g11", "g14"]

# Open websockets
CONNECTIONS: set[WebsocketConnection] = set()

# Map from room name to presence expiry time (or True if waiting for presence sensor to fade)
ROOM_STATES: dict[str, datetime | bool] = {}

# Map from (type, target) to state
CACHED_STATES: dict[tuple[str, str], str] = {}


@dataclass
class WebsocketMessage:
    # Shown on the log
    display: str | None
    # Targets an SVG element
    type: str | None
    target: str | None
    # Sets a class on that element
    state: str | None


async def new_websocket(websocket: WebsocketConnection):
    """Record a new websocket connection"""
    CONNECTIONS.add(websocket)
    try:
        # Send cached state so it's up to date
        for (type, target), state in CACHED_STATES.items():
            msg = WebsocketMessage(None, type, target, state)
            print(msg) if DEBUG else ""
            await websocket.send(json.dumps(dataclasses.asdict(msg)))
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)


async def subscribe_topics(client, _userdata, _flags_dict, _result):
    """Subscribe to MQTT topics for a new connection"""
    await client.asyncio_subscribe("doorman/+/user")
    # await client.asyncio_subscribe("sensor/+/presence")
    await client.asyncio_subscribe("tool/+/user")


async def doorman_message(msg):
    """Handle a doorman MQTT message, from doorman/+/user"""
    name: str = msg.payload.decode("utf-8")
    if len(name) == 0:
        # Door closing again, ignore
        return

    # topic is of the form doorman/<room>/user
    room = msg.topic.split("/")[1]

    if name == "anonymous" or room not in ROOM_WHITELIST:
        return

    # mark the room as active for some period of time, to get around the presence sensors sucking ass
    ROOM_STATES[room] = datetime.now() + ROOM_ACTIVE_TIME
    await send_message(
        WebsocketMessage(
            f"<span class=username>{name}</span> entered <span class=room>{room}</span>",
            "room",
            room,
            "active",
        )
    )


async def presence_message(msg):
    """Handle a presence MQTT message, from sensor/+/presence"""
    # topic is of the form sensor/<room>/presence
    room = msg.topic.split("/")[1]
    state: str = msg.payload.decode("utf-8")

    if room == "global":
        # special thing we don't care about
        return

    if state == "active":
        # only display a message if room isn't already active
        do_display = room not in ROOM_STATES
        # don't expire the room state as we'll get an empty message
        ROOM_STATES[room] = True
        await send_message(
            WebsocketMessage(
                f"someone is in <span class=room>{room}</span>" if do_display else None,
                "room",
                room,
                "active",
            )
        )
    elif state == "empty":
        do_display = room in ROOM_STATES
        if do_display:
            del ROOM_STATES[room]
        await send_message(
            WebsocketMessage(
                f"<span class=room>{room}</span> is now empty" if do_display else None,
                "room",
                room,
                "inactive",
            )
        )


async def tool_message(msg):
    """Handle a tool status MQTT message, from tool/+/user"""
    # topic is of the form tool/<room>/user
    tool = msg.topic.split("/")[1]
    name: str = msg.payload.decode("utf-8")

    if len(name) == 0:
        await send_message(
            WebsocketMessage(
                f"<span class=tool>{tool}</span> no longer in use",
                "tool",
                tool,
                "inactive",
            )
        )
    elif name != "anonymous":
        await send_message(
            WebsocketMessage(
                f"<span class=username>{name}</span> is now using <span class=tool>{tool}</span>",
                "tool",
                tool,
                "active",
            )
        )


async def mqtt_message(_client, _userdata, msg: MQTTMessage):
    """Dispatch MQTT message to the correct handler"""
    try:
        if msg.topic.startswith("doorman/") and msg.topic.endswith("/user"):
            await doorman_message(msg)
        elif msg.topic.startswith("sensor/") and msg.topic.endswith("/presence"):
            await presence_message(msg)
        elif msg.topic.startswith("tool/") and msg.topic.endswith("/user"):
            await tool_message(msg)
    except Exception as e:
        print(f"Error processing message: {e}")


async def event_loop():
    client = AsyncioPahoClient()
    client.asyncio_listeners.add_on_connect(subscribe_topics)
    client.asyncio_listeners.add_on_message(mqtt_message)
    await client.asyncio_connect(MQTT_HOST)

    while True:
        await asyncio.sleep(ROOM_EXPIRY_POLL_SECS)
        try:
            for room in list(
                ROOM_STATES.keys()
            ):  # needed because dictionary size will change
                expiry = ROOM_STATES[room]
                if type(expiry) is datetime and expiry <= datetime.now():
                    del ROOM_STATES[room]
                    await send_message(
                        WebsocketMessage(
                            None,
                            "room",
                            room,
                            "inactive",
                        )
                    )
        except Exception as e:
            print(f"Error in event loop: {e}")


async def send_message(msg: WebsocketMessage):
    print(msg) if DEBUG else ""
    if msg.state != None and msg.type != None and msg.target != None:
        CACHED_STATES[(msg.type, msg.target)] = msg.state

    broadcast(CONNECTIONS, json.dumps(dataclasses.asdict(msg)))


# Code for testing without MQTT
# MESSAGES = [
#     WebsocketMessage(
#         "<span class=username>aria</span> started using lasercutter",
#         "tool",
#         "lasercutter",
#         "active",
#     ),
#     WebsocketMessage(
#         "<span class=tool>lasercutter</span> is no longer in use",
#         "tool",
#         "lasercutter",
#         "inactive",
#     ),
#     WebsocketMessage(
#         "<span class=username>aria</span> started using lasercutter2",
#         "tool",
#         "lasercutter2",
#         "active",
#     ),
#     WebsocketMessage(
#         "<span class=tool>lasercutter2</span> is no longer in use",
#         "tool",
#         "lasercutter2",
#         "inactive",
#     ),
#     WebsocketMessage(
#         "<span class=username>aria</span> started using robotarm",
#         "tool",
#         "robotarm",
#         "active",
#     ),
#     WebsocketMessage(
#         "<span class=tool>robotarm</span> is no longer in use",
#         "tool",
#         "robotarm",
#         "inactive",
#     ),
#     WebsocketMessage(
#         "<span class=username>aria</span> started using lathe",
#         "tool",
#         "lathe",
#         "active",
#     ),
#     WebsocketMessage(
#         "<span class=tool>lathe</span> is no longer in use",
#         "tool",
#         "lathe",
#         "inactive",
#     ),
#     WebsocketMessage(
#         "<span class=username>aria</span> started using bandsaw",
#         "tool",
#         "bandsaw",
#         "active",
#     ),
#     WebsocketMessage(
#         "<span class=tool>bandsaw</span> is no longer in use",
#         "tool",
#         "bandsaw",
#         "inactive",
#     ),
#     WebsocketMessage(
#         "<span class=username>aria</span> started using sander",
#         "tool",
#         "sander",
#         "active",
#     ),
#     WebsocketMessage(
#         "<span class=tool>sander</span> is no longer in use",
#         "tool",
#         "sander",
#         "inactive",
#     ),
#     WebsocketMessage(
#         "<span class=username>aria</span> started using cncrouter",
#         "tool",
#         "cncrouter",
#         "active",
#     ),
#     WebsocketMessage(
#         "<span class=tool>cncrouter</span> is no longer in use",
#         "tool",
#         "cncrouter",
#         "inactive",
#     ),
#     WebsocketMessage(
#         "<span class=username>aria</span> started using sewingmachine",
#         "tool",
#         "sewingmachine",
#         "active",
#     ),
#     WebsocketMessage(
#         "<span class=tool>sewingmachine</span> is no longer in use",
#         "tool",
#         "sewingmachine",
#         "inactive",
#     ),
#     WebsocketMessage(
#         "<span class=username>aria</span> entered <span class=room>g1</span>",
#         "room",
#         "g1",
#         "active",
#     ),
#     WebsocketMessage(
#         None,
#         "room",
#         "g1",
#         "inactive",
#     ),
#     WebsocketMessage(
#         "<span class=username>aria</span> entered <span class=room>g8</span>",
#         "room",
#         "g8",
#         "active",
#     ),
#     WebsocketMessage(
#         None,
#         "room",
#         "g8",
#         "inactive",
#     ),
#     WebsocketMessage(
#         "<span class=username>aria</span> entered <span class=room>g11</span>",
#         "room",
#         "g11",
#         "active",
#     ),
#     WebsocketMessage(
#         None,
#         "room",
#         "g11",
#         "inactive",
#     ),
#     WebsocketMessage(
#         "<span class=username>aria</span> entered <span class=room>g14</span>",
#         "room",
#         "g14",
#         "active",
#     ),
#     WebsocketMessage(
#         None,
#         "room",
#         "g14",
#         "inactive",
#     ),
#     WebsocketMessage(
#         "<span class=username>aria</span> entered <span class=room>g2</span>",
#         "room",
#         "g2",
#         "active",
#     ),
#     WebsocketMessage(
#         None,
#         "room",
#         "g2",
#         "inactive",
#     ),
# ]


# async def mock_events():
#     i = 0
#     while True:
#         await send_message(MESSAGES[i])
#         print(MESSAGES[i])
#         i = (i + 1) % len(MESSAGES)
#         await asyncio.sleep(0.2)


async def main():
    async with serve(new_websocket, WEBSOCKET_BIND[0], WEBSOCKET_BIND[1]):
        await event_loop()  # runs forever
        # await mock_events()  # runs forever


if __name__ == "__main__":
    asyncio.run(main())

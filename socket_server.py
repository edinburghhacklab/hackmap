#!/usr/bin/env python
import asyncio
import json

from websockets.asyncio.server import broadcast, serve
from websockets.frames import CloseCode


CONNECTIONS = set()


async def handler(websocket):
    """Authenticate user and register connection in CONNECTIONS."""
    CONNECTIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)


MESSAGES = [
    {
        "display": "<span class=username>aria</span> entered <span class=target>g1</span>",
        "target": "g1",
        "type": "room",
        "state": "active",
    },
    {
        "display": "<span class=target>g2</span> is now empty",
        "target": "g2",
        "type": "room",
        "state": "inactive",
    },
    {
        "display": "<span class=username>yasha</span> entered <span class=target>g8</span>",
        "target": "g8",
        "type": "room",
        "state": "active",
    },
    {
        "display": "<span class=target>g1</span> is now empty",
        "target": "g1",
        "type": "room",
        "state": "inactive",
    },
    {
        "display": "<span class=username>costa</span> entered <span class=target>g11</span>",
        "target": "g11",
        "type": "room",
        "state": "active",
    },
    {
        "display": "<span class=target>g8</span> is now empty",
        "target": "g8",
        "type": "room",
        "state": "inactive",
    },
    {
        "display": "<span class=username>anonymous</span> entered <span class=target>g14</span>",
        "target": "g14",
        "type": "room",
        "state": "active",
    },
    {
        "display": "<span class=target>g11</span> is now empty",
        "target": "g11",
        "type": "room",
        "state": "inactive",
    },
    {
        "display": "<span class=username>cazagen</span> entered <span class=target>g2</span>",
        "target": "g2",
        "type": "room",
        "state": "active",
    },
    {
        "display": "<span class=target>g14</span> is now empty",
        "target": "g14",
        "type": "room",
        "state": "inactive",
    },
]


async def process_events():
    i = 0
    while True:
        broadcast(CONNECTIONS, json.dumps(MESSAGES[i]))
        print(MESSAGES[i])
        i = (i + 1) % len(MESSAGES)
        await asyncio.sleep(2.0)


async def main():
    async with serve(handler, "localhost", 8001):
        await process_events()  # runs forever


if __name__ == "__main__":
    asyncio.run(main())

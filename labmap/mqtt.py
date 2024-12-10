import paho.mqtt.client as mqtt
from django.conf import settings

_client = mqtt.Client()
_client_started = False


def connect():
    global _client_started
    if hasattr(settings, "MQTT_HOST") and hasattr(settings, "MQTT_PORT"):
        if _client_started is False:
            try:
                _client.connect(settings.MQTT_HOST, settings.MQTT_PORT)
                _client.loop_start()
                _client_started = True
                print("mqtt client started")
            except ConnectionRefusedError:
                print("mqtt client not started")


def client():
    if _client_started is False:
        connect()
    return _client

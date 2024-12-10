from django.conf import settings


def settings_context(request):
    return {
        "MQTT_WS_URL": f"ws://{settings.MQTT_HOST}:{settings.MQTT_WS_PORT}/mqtt",
    }

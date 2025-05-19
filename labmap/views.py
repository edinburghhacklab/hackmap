from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import labmap.mqtt


def map(req: HttpRequest) -> HttpResponse:
    return render(req, "map.html")


def lights(req: HttpRequest) -> HttpResponse:
    return render(
        req,
        "lights.html",
        context={
            "is_kiosk": req.GET.get("kiosk", False) != False,
        },
    )


@require_POST
@csrf_exempt
def set_lights(req: HttpRequest, ids: str, val: int) -> JsonResponse:
    mqtt = labmap.mqtt.client()
    lights = ids.split(",")
    for light in lights:
        try:
            light_id = int(light)
            assert light_id < 18
            mqtt.publish(f"dali/g1/set/{light_id}", payload=val)
        except Exception as e:
            print(e)
            continue
    return JsonResponse({})


@require_POST
@csrf_exempt
def set_light_preset(req: HttpRequest, preset: str) -> JsonResponse:
    if preset not in [
        "off",
        "dim",
        "bright",
        "corners",
        "movie",
        "comfort",
        "presentation",
        "harmony",
        "random",
    ]:
        return JsonResponse({"msg": "unrecognised preset"})

    mqtt = labmap.mqtt.client()
    mqtt.publish(f"dali/g1/preset/{preset}")
    return JsonResponse({})

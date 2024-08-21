from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.conf import settings


def map(req: HttpRequest) -> HttpResponse:
    return render(
        req, "map.html", context={"websocket_url": settings.MAP_WEBSOCKET_URL}
    )

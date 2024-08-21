from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def hello(req: HttpRequest) -> HttpResponse:
    return render(req, "map.html")


# Create your views here.

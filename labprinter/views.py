from django.shortcuts import render
from labprinter.models import Printer
from django.views.generic.list import ListView
import labdash.mqtt
from django.http import JsonResponse


class Printers(ListView):
    model = Printer
    context_object_name = "printers"
    queryset = Printer.objects.all().order_by("shortname")


def lights_on(request):
    mqtt = labdash.mqtt.client()
    for printer in Printer.objects.all().exclude(led_topic__exact=""):
        mqtt.publish(printer.led_topic, payload="1")

    return JsonResponse({"status": "ok"})


def lights_off(request):
    mqtt = labdash.mqtt.client()
    for printer in Printer.objects.all().exclude(led_topic__exact=""):
        mqtt.publish(printer.led_topic, payload="0")

    return JsonResponse({"status": "ok"})

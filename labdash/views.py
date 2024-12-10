from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from labdash.models import ButtonGroup, Button, Slider
import labdash.mqtt


class Dashboard(ListView):
    model = ButtonGroup
    context_object_name = "groups"
    queryset = ButtonGroup.objects.order_by("priority")


def trigger_button(request, pk):
    btn = get_object_or_404(Button, pk=pk)
    mqtt = labdash.mqtt.client()
    for action in btn.actions.all():
        mqtt.publish(action.topic, payload=action.payload, retain=action.retain)
    return JsonResponse({"status": "ok"})


def trigger_slider(request, pk, val):
    slider = get_object_or_404(Slider, pk=pk)
    mqtt = labdash.mqtt.client()
    norm_val = max(0.0, min(1.0, float(val)))
    for action in slider.actions.all():
        payload = int(action.min + (norm_val * (action.max - action.min)))
        mqtt.publish(action.topic, payload=payload, retain=action.retain)
    return JsonResponse({"status": "ok"})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from labdash.models import ButtonGroup, Button
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

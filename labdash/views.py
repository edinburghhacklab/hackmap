from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from labdash.models import ButtonGroup, Button
import labdash.mqtt


class Dashboard(ListView):
    model = ButtonGroup
    context_object_name = "groups"
    queryset = ButtonGroup.objects.filter(screen="main", hide=False).order_by(
        "priority"
    )


def custom_screen(req, name):
    groups = (
        ButtonGroup.objects.filter(screen=name, hide=False).order_by("priority").all()
    )
    return render(
        req,
        "labdash/buttongroup_list.html",
        context={
            "groups": groups,
            "do_home_timeout": req.GET.get("kiosk", False) != False,
        },
    )


def trigger_button(request, pk):
    btn = get_object_or_404(Button, pk=pk)
    mqtt = labdash.mqtt.client()
    for action in btn.actions.all():
        mqtt.publish(action.topic, payload=action.payload, retain=action.retain)
    return JsonResponse({"status": "ok"})

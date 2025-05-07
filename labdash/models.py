from django.db import models


class ButtonGroup(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    priority = models.IntegerField(default=50)
    tile_width = models.IntegerField(default=1)
    hide = models.BooleanField(default=False)
    buttons: models.QuerySet["Button"]

    def __str__(self):
        return self.name

    def get_buttons(self):
        return self.buttons.order_by("priority").all()


class Button(models.Model):
    name = models.CharField(max_length=200)
    icon = models.FileField()
    group = models.ForeignKey(
        ButtonGroup, related_name="buttons", on_delete=models.CASCADE
    )
    priority = models.IntegerField(default=50)
    subscribe_topic = models.CharField(max_length=200, default="", blank=True)
    subscribe_value = models.CharField(max_length=200, default="", blank=True)
    href = models.CharField(max_length=50, blank=True, default="")
    actions: models.QuerySet["Action"]

    def __str__(self):
        return self.name


class Action(models.Model):
    button = models.ForeignKey(Button, related_name="actions", on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    retain = models.BooleanField(default=False)
    payload = models.CharField(max_length=200, blank=True, null=True)

from django.db import models


class ButtonGroup(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    lighttext = models.BooleanField(default=False)
    priority = models.IntegerField(default=50)
    tile_width = models.CharField(max_length=50, default="two")

    def __str__(self):
        return self.name

    def get_buttons(self):
        return self.buttons.order_by("priority").all()

    def get_sliders(self):
        return self.sliders.order_by("priority").all()


class Button(models.Model):
    name = models.CharField(max_length=200)
    icon = models.FileField()
    group = models.ForeignKey(
        ButtonGroup, related_name="buttons", on_delete=models.CASCADE
    )
    priority = models.IntegerField(default=50)
    subscribe_topic = models.CharField(max_length=200, default="", blank=True)
    subscribe_value = models.CharField(max_length=200, default="", blank=True)

    def __str__(self):
        return self.name


class Action(models.Model):
    button = models.ForeignKey(Button, related_name="actions", on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    retain = models.BooleanField(default=False)
    payload = models.CharField(max_length=200, blank=True, null=True)


class Slider(models.Model):
    name = models.CharField(max_length=200)
    group = models.ForeignKey(
        ButtonGroup, related_name="sliders", on_delete=models.CASCADE
    )
    priority = models.IntegerField(default=50)

    def __str__(self):
        return self.name


class SliderAction(models.Model):
    slider = models.ForeignKey(Slider, related_name="actions", on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=255)

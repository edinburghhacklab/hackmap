from django.db import models


class Printer(models.Model):
    name = models.CharField(max_length=200)
    shortname = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    color = models.CharField(max_length=20, default="black")
    camera_url = models.CharField(max_length=300, blank=True, default="")
    led_topic = models.CharField(max_length=300, blank=True, default="")

    def __str__(self):
        return self.name

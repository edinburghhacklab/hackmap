from django.db import models


class Printer(models.Model):
    name = models.CharField(max_length=200)
    shortname = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    color = models.CharField(max_length=20, default="black")

    def __str__(self):
        return self.name

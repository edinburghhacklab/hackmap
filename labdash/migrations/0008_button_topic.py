# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labdash", "0007_slider_slideraction"),
    ]

    operations = [
        migrations.AddField(
            model_name="button",
            name="subscribe_topic",
            field=models.CharField(max_length=200, default=""),
        ),
        migrations.AddField(
            model_name="button",
            name="subscribe_value",
            field=models.CharField(max_length=200, default=""),
        ),
    ]

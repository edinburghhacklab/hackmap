# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labdash", "0008_button_topic"),
    ]

    operations = [
        migrations.AddField(
            model_name="buttongroup",
            name="tile_width",
            field=models.CharField(max_length=50, default="two"),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-14 01:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("labdash", "0003_auto_20161213_2022"),
    ]

    operations = [
        migrations.CreateModel(
            name="Action",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("topic", models.CharField(max_length=200)),
                ("payload", models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="button",
            name="payload",
        ),
        migrations.RemoveField(
            model_name="button",
            name="topic",
        ),
        migrations.AddField(
            model_name="action",
            name="button",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="actions",
                to="labdash.Button",
            ),
        ),
    ]

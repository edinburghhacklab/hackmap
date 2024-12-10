# Generated by Django 5.1 on 2024-12-10 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labdash', '0009_buttongroup_width'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slideraction',
            name='slider',
        ),
        migrations.AlterField(
            model_name='action',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='button',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='button',
            name='subscribe_topic',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='button',
            name='subscribe_value',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='buttongroup',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.DeleteModel(
            name='Slider',
        ),
        migrations.DeleteModel(
            name='SliderAction',
        ),
    ]
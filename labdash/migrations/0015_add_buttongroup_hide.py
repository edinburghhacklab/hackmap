from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("labdash", "0014_alter_button_href"),
    ]

    operations = [
        migrations.AddField(
            model_name="buttongroup",
            name="hide",
            field=models.BooleanField(default=False),
        ),
    ]

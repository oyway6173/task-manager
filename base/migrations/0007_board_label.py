# Generated by Django 4.1.3 on 2023-07-14 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0006_status_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="board",
            name="label",
            field=models.CharField(default="#default_label", max_length=50),
        ),
    ]
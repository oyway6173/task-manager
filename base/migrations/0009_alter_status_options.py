# Generated by Django 4.1.3 on 2023-07-15 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0008_alter_status_options"),
    ]

    operations = [
        migrations.AlterModelOptions(name="status", options={"ordering": ["step"]},),
    ]

# Generated by Django 4.1.3 on 2023-07-13 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_alter_issue_project"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="bio",
            field=models.TextField(blank=True, null=True),
        ),
    ]

# Generated by Django 3.1.2 on 2020-10-22 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_newregistration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newregistration",
            name="choices",
            field=models.CharField(default="", max_length=1024),
            preserve_default=False,
        ),
    ]

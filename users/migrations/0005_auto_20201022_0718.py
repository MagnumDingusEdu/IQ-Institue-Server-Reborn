# Generated by Django 3.1.2 on 2020-10-22 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201022_0713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newregistration',
            old_name='choices',
            new_name='courses',
        ),
    ]

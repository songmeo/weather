# Generated by Django 3.1.1 on 2020-09-16 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0026_parameter_values'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parameter',
            name='values',
        ),
    ]

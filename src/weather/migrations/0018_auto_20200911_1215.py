# Generated by Django 3.1.1 on 2020-09-11 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0017_auto_20200911_0838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parameter',
            name='avg',
        ),
        migrations.RemoveField(
            model_name='parameter',
            name='max',
        ),
        migrations.RemoveField(
            model_name='parameter',
            name='min',
        ),
    ]
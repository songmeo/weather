# Generated by Django 3.1.1 on 2020-09-07 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0004_auto_20200906_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameter',
            name='values',
            field=models.JSONField(default={}),
        ),
    ]

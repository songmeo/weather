# Generated by Django 3.1.1 on 2020-09-10 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0011_auto_20200910_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='ref',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]

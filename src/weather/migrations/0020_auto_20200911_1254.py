# Generated by Django 3.1.1 on 2020-09-11 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0019_auto_20200911_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='_city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='weather.city'),
        ),
    ]
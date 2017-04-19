# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-19 21:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ParkSpot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lng', models.FloatField(blank=True, null=True)),
                ('radius', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParkSpotReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
                ('parkspot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parkingspot.ParkSpot')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

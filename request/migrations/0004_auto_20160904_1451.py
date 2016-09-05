# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-04 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0003_auto_20160904_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcerequest',
            name='accomodation_at',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='resourcerequest',
            name='flight_from',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='resourcerequest',
            name='flight_to',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='resourcerequest',
            name='forex_details',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='resourcerequest',
            name='laptop_config',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='resourcerequest',
            name='passport',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]

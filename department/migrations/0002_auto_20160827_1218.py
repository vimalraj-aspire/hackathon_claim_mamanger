# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-27 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeerole',
            name='role',
            field=models.IntegerField(default=2),
        ),
    ]
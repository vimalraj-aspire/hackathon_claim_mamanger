# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0004_auto_20160825_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='state',
            field=models.IntegerField(choices=[(0, b'Intiated'), (1, b'Approved'), (2, b'Rejected')], default=0),
        ),
    ]
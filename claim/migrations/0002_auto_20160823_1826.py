# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-23 18:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claim',
            name='employee',
        ),
        migrations.AddField(
            model_name='claim',
            name='image',
            field=models.FileField(default=0, upload_to='claim_documents'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='claim',
            name='owner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]

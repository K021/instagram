# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-16 01:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0011_auto_20171014_2136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='text',
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]

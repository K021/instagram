# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 22:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0009_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='nickname', max_length=50),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-14 12:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_post_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(blank=True, choices=[('Audio', (('vinyl', 'Vinyl'), ('cd', 'CD'))), ('Video', (('vhs', 'VHS Tape'), ('dvd', 'DVD'))), ('unknown', 'Unknown'), ('', 'Nothing to add')], max_length=50, null=True),
        ),
    ]

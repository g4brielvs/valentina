# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-11 13:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(1970, 1, 1, 0, 0), verbose_name='criado em'),
            preserve_default=False,
        ),
    ]

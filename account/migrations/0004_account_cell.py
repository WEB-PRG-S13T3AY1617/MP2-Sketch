# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-28 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20170727_0238'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='cell',
            field=models.CharField(default='+00 000 000 0000', max_length=20),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 14:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=15)),
                ('use', models.CharField(default='office', max_length=8)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('tags', models.TextField(max_length=255)),
                ('picture', models.ImageField(default='default.png', upload_to='items/%Y/%m/%d')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-19 20:19
from __future__ import unicode_literals

from django.db import migrations, models
import libs.utils.string_extension


class Migration(migrations.Migration):

    dependencies = [
        ('cryapp', '0004_auto_20170519_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryorder',
            name='id',
            field=models.CharField(default=libs.utils.string_extension.get_uuid, max_length=32, primary_key=True, serialize=False, verbose_name='id'),
        ),
    ]
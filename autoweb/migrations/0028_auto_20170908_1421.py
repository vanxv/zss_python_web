# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-08 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoweb', '0027_auto_20170908_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobileid',
            name='QQ',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-07 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoweb', '0022_auto_20170907_1555'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='qqgrouplistlog',
            options={'verbose_name': 'QQGroupListlog', 'verbose_name_plural': 'QQGroupListlog'},
        ),
        migrations.AlterField(
            model_name='qqgrouplist',
            name='QQ',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='qqgrouplistlog',
            name='QQ',
            field=models.CharField(max_length=20, null=True),
        ),
    ]

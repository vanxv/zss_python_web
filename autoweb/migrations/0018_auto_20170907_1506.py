# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-07 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoweb', '0017_mobileid_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='qqgrouplist',
            name='contains',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='qqgrouplist',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
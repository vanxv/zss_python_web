# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-19 17:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cryapp', '0004_auto_20170619_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryorder',
            name='Userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Userid', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cryorder',
            name='buyerid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyerid', to=settings.AUTH_USER_MODEL),
        ),
    ]
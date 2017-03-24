# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 17:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='good',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shop',
        ),
        migrations.AddField(
            model_name='order',
            name='good_id',
            field=models.IntegerField(null=True, verbose_name='商品'),
        ),
        migrations.AddField(
            model_name='order',
            name='shop_id',
            field=models.IntegerField(null=True, verbose_name='店铺'),
        ),
    ]
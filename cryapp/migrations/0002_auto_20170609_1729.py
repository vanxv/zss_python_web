# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-09 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryorder',
            name='Status',
            field=models.IntegerField(choices=[(0, '关闭'), (1, '启动'), (2, '接任务'), (3, '提交等待审核'), (4, '审核不通过'), (5, '完成')], verbose_name='状态启动与关闭'),
        ),
    ]
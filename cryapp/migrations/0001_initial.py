# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-30 10:21
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import libs.utils.string_extension


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryOrder',
            fields=[
                ('id', models.CharField(default=libs.utils.string_extension.get_uuid, max_length=32, primary_key=True, serialize=False, verbose_name='id')),
                ('Money', models.FloatField(verbose_name='交易金额')),
                ('Keywords', models.CharField(max_length=20, verbose_name='关键词')),
                ('platform', models.CharField(choices=[('taobao', 'taobao'), ('jd', 'jd'), ('tmall', 'tmall'), ('1688', '1688')], max_length=20, null=True, verbose_name='店铺平台')),
                ('OrderSort', models.IntegerField(choices=[(1, '红包任务'), (2, '好评返现'), (3, '免费试用')], null=True, verbose_name='订单分类')),
                ('Status', models.IntegerField(choices=[(0, '关闭'), (1, '启动'), (2, '接任务'), (3, '提交等待审核'), (4, '审核通过'), (5, '完成')], verbose_name='状态启动与关闭')),
                ('StartTime', models.DateField(verbose_name='startTime开始时间')),
                ('EndTime', models.DateField(verbose_name='EndTime结束时间')),
                ('AddTime', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('Note', models.CharField(max_length=1200, verbose_name='备注')),
                ('GoodId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='GoodsId')),
                ('ShopId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Shop', verbose_name='Shopid')),
                ('Userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='UserId卖家')),
                ('buyerid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='index', to=settings.AUTH_USER_MODEL, verbose_name='buyerId买家')),
            ],
            options={
                'verbose_name': '试用任务表',
                'verbose_name_plural': '试用任务表',
            },
        ),
    ]

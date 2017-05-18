# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-09 09:29
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cashback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField(null=True, verbose_name='任务id')),
                ('customer_id', models.IntegerField(null=True, verbose_name='会员id')),
                ('wechat', models.CharField(blank=True, max_length=50, null=True, verbose_name='会员微信')),
                ('alipay', models.CharField(blank=True, max_length=50, null=True, verbose_name='会员支付宝账号')),
                ('orderno', models.CharField(blank=True, max_length=100, null=True, verbose_name='订单号')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True, verbose_name='返现金额')),
                ('certificate', models.CharField(blank=True, max_length=200, null=True, verbose_name='好评凭证')),
                ('showpic1', models.CharField(blank=True, max_length=200, null=True, verbose_name='买家秀')),
                ('showpic2', models.CharField(blank=True, max_length=200, null=True, verbose_name='买家秀')),
                ('status', models.IntegerField(choices=[(1, '待审核'), (2, '审核通过，等待平台打款'), (3, '关闭申请'), (4, '已完成')], null=True, verbose_name='状态')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='商家')),
            ],
            options={
                'verbose_name': '返现',
                'verbose_name_plural': '返现列表',
                'db_table': 'cashbacks',
            },
        ),
        migrations.CreateModel(
            name='CashbackTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_id', models.IntegerField(null=True, verbose_name='商家id')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='名称')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True, verbose_name='返现金额')),
                ('max_count', models.IntegerField(null=True, verbose_name='最大参与人数')),
                ('expiretime', models.DateTimeField(blank=True, null=True, verbose_name='截止时间')),
                ('remark', models.CharField(max_length=200, null=True, verbose_name='备注')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'cashback_tasks',
            },
        ),
        migrations.CreateModel(
            name='CashbackTaskGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_id', models.IntegerField(null=True, verbose_name='商家id')),
                ('task_id', models.IntegerField(null=True, verbose_name='任务id')),
                ('shop_id', models.CharField(max_length=32, null=True, verbose_name='店铺id')),
                ('goods_id', models.CharField(max_length=32, null=True, verbose_name='商品id')),
            ],
            options={
                'db_table': 'cashback_task_goods',
            },
        ),
        migrations.CreateModel(
            name='Sendsms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_id', models.IntegerField(null=True, verbose_name='商家id')),
                ('customer_id', models.IntegerField(null=True, verbose_name='会员id')),
                ('mobile', models.CharField(blank=True, max_length=20, null=True, verbose_name='手机号')),
                ('content', models.CharField(blank=True, max_length=200, null=True, verbose_name='内容')),
                ('captcha', models.CharField(blank=True, max_length=100, null=True, verbose_name='验证码')),
                ('is_success', models.NullBooleanField(verbose_name='发送是否成功')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'sendsms',
            },
        ),
        migrations.CreateModel(
            name='WXOfficialConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(null=True, verbose_name='商家id')),
                ('appid', models.CharField(blank=True, max_length=200, null=True)),
                ('appsecret', models.CharField(blank=True, max_length=200, null=True)),
                ('mchid', models.CharField(blank=True, max_length=200, null=True)),
                ('key', models.CharField(max_length=200, null=True)),
                ('apptoken', models.CharField(max_length=200, null=True)),
                ('encodingaeskey', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'wxofficial_config',
            },
        ),
    ]
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       Administrator
    @   date    :       2019/7/17 22:48
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :       
-------------------------------------------------
"""
# 订单管理model
from app.dbengines import db
import datetime
from Task import Task


class TaskOrder(db.Document):
    openid = db.StringField(max_length=255, verbose_name='微信openid')

    out_trade_no = db.StringField(max_length=255, verbose_name='商户订单号')
    body = db.StringField(max_length=255, verbose_name='商品简单描述')
    total_fee = db.FloatField(verbose_name='订单总金额')
    pay_type = db.IntField(default=1, verbose_name='付款方式（1：微信 2：支付宝）')
    ischeck = db.IntField(verbose_name='支付状态（1：已支付 2：未支付）')  # 已支付，未支付  1
    status = db.IntField(verbose_name='当前订单状态（1：支付成功 2：支付中 4：支付失败')  # 支付中，，支付成功，支付失败
    create_time = db.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')
    betting_type = db.IntField(verbose_name='投注类型：（1：成功 2：失败）')
    task = db.ReferenceField(Task)

    def __unicode__(self):
        return str(self.out_trade_no)

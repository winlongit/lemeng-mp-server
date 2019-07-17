#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       Administrator
    @   date    :       2019/7/18 0:08
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :       
-------------------------------------------------
"""
from app.dbengines import db
import datetime
from Task import Task
from User import User


class TaskRecord(db.Document):
    user = db.ReferenceField(User, verbose_name='哪个用户对这个挑战操作')
    task = db.ReferenceField(Task, verbose_name='对哪个挑战操作')
    record_type = db.IntField(verbose_name='时间类型：（1：投注 2：评论）')
    betting_type = db.IntField(verbose_name='投注类型：（1：成功 2：失败）')
    betting_amount = db.IntField(verbose_name='投注金额')
    comment = db.StringField(max_length=1024, verbose_name='评论内容')
    create_time = db.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')

    def __unicode__(self):
        return str(self.out_trade_no)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       Administrator
    @   date    :       2019/7/13 23:30
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :       
-------------------------------------------------
"""
import datetime

from app.dbengines import db


class Picture(db.Document):
    creator = db.StringField(max_length=255, verbose_name='上传者，创建人 id')

    image = db.ImageField(verbose_name='图片', thumbnail_size=(200, 200, True))
    img_type = db.StringField(max_length=64, verbose_name='图片type')
    family = db.StringField(max_length=64, verbose_name='分类')
    create_time = db.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')

    def __unicode__(self):
        return str(self.creator)

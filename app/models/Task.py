#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       Administrator
    @   date    :       2019/7/13 10:26
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :       
-------------------------------------------------
"""
# 这里使用 from db import db ,不要用 from . import db ( from . 就是从 __init__ 中找，__init__ 需要依赖咱们，咱们又去依赖 __init__，造成循环依赖，应该避免这种情况)
from app.dbengines import db
import datetime
from Picture import Picture

class Task(db.Document):
    """
    Supported fields

        StringField
        BinaryField
        URLField
        EmailField
        IntField
        FloatField
        DecimalField
        BooleanField
        DateTimeField
        ListField (using wtforms.fields.FieldList )
        SortedListField (duplicate ListField)
    EmbeddedDocument是包含在父Document里的一组数据，没有单独的Collection。
    ReferenceDocument有自己独立的Collection，引用它的Docuemnt中只包含一个Id
        EmbeddedDocumentField (using wtforms.fields.FormField and generating inline Form)
        ReferenceField (using wtforms.fields.SelectFieldBase with options loaded from QuerySet or Document)
        DictField
    """
    creator_openid = db.StringField(max_length=255, verbose_name='创建人：用户在小程序中对应的 openid')

    title = db.StringField(max_length=255, verbose_name='标题')
    current_weight = db.IntField(verbose_name='当前体重')
    goal_weight = db.IntField(verbose_name='目标体重')
    task_image = db.ReferenceField(Picture, verbose_name='封面配图')
    dead_line = db.DateTimeField(verbose_name='挑战设定的 结束时间,到期时间')
    status = db.IntField(verbose_name='任务状态：（1：初始化刚、创建）（ 2：进行中） （4：成功结束）（8：失败结束)')
    complete_time = db.DateTimeField(verbose_name='挑战实际的 结束时间,到期时间')
    create_time = db.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')
    challenge_success_betting = db.IntField(verbose_name='胜利投注总金额，单位是分')
    challenge_fail_betting = db.IntField(verbose_name='失败投注总金额，单位是分')

    meta = {'allow_inheritance': True}

    def __unicode__(self):
        return str(self.name)


"""    def get_list_image(self):
        obj = self.task_image
        if not obj.grid_id:
            return ''
        return "/img/%s" % (str(obj.grid_id))
"""

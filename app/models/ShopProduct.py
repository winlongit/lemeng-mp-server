# -*- coding: UTF-8 -*-
from app.dbengines import db
import datetime


# 订单管理model
class Product(db.Document):
    name = db.StringField(max_length=255, verbose_name='名称')
    price = db.StringField(max_length=255, verbose_name='价格(整数:元)')
    type = db.StringField(max_length=255, verbose_name='产品分类')
    test_type = db.StringField(max_length=255, verbose_name='检测方式')
    post_type = db.StringField(max_length=255, verbose_name='配送方式')

    send_address = db.StringField(max_length=255, verbose_name='送检地址')
    send_note = db.StringField(verbose_name='送检说明')
    list_pic = db.ImageField(verbose_name='列表配图')
    list_desc = db.StringField(max_length=255, verbose_name='列表描述')  # 列表简介
    desc_pic = db.ImageField(verbose_name='详情大图')
    desc_detail = db.ImageField(verbose_name='产品简介')  # 详细项目简介
    desc_content = db.ImageField(verbose_name='检测内容')  # 详细检测内容
    desc_note = db.ImageField(verbose_name='注意事项')  # 详细注意事项
    prod_info = db.StringField(verbose_name='产品信息')  # 项目所需填写内容
    prod_template = db.StringField(verbose_name='产品模板URL')  # 项目所需填写模板

    known_issues = db.StringField(verbose_name='知情同意书')  # 知情同意书
    known_issues_patient = db.StringField(verbose_name='受检者同意书')  # 受检者同意书

    sender = db.StringField(max_length=255, verbose_name='发件寄件人')
    sender_phone = db.StringField(max_length=255, verbose_name='发件寄件手机')
    sender_address = db.StringField(max_length=255, verbose_name='发件寄件地址')

    returner = db.StringField(max_length=255, verbose_name='回单收件人')
    returner_phone = db.StringField(max_length=255, verbose_name='回单收件手机')
    returner_address = db.StringField(max_length=255, verbose_name='回单收件地址')
    tubetype = db.StringField(max_length=255, verbose_name='试管类型')
    taketime = db.StringField(max_length=255, verbose_name='取单时间')


    credit = db.IntField(default=0, verbose_name='积分')

    create_time = db.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')
    hide = db.BooleanField(default=False, verbose_name='隐藏')

    def __unicode__(self):
        return str(self.name)

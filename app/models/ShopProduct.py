# -*- coding: UTF-8 -*-
from app.dbengines import db
from Picture import Picture
import datetime


class OnePicture(db.EmbeddedDocument):
    order = db.IntField(min_value=1, verbose_name="一组图片中，这张图片的序号")
    pic_id = db.ReferenceField(Picture, verbose_name="图片在Picture表中的id")


# 产品model
class Product(db.Document):
    name = db.StringField(max_length=255, verbose_name='商品名称')
    description = db.StringField(max_length=255, verbose_name='商品描述')
    price = db.IntField(verbose_name='价格(整数:分)，注意单位是分')
    type = db.StringField(max_length=255, verbose_name='产品分类-一级分类')
    category = db.StringField(max_length=255, verbose_name='产品分类-二级分类')
    specification = db.ListField(db.StringField(max_length=255, verbose_name="规格"))

    list_swipers = db.ListField(db.EmbeddedDocumentField(OnePicture, verbose='轮播图list'))
    list_desc = db.ListField(db.EmbeddedDocumentField(OnePicture, verbose='详情图list'))

    state = db.StringField(max_length=16, default="待上架", verbose_name='商品状态：已上架，待上架，已下架')

    create_time = db.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')

    def __unicode__(self):
        return str(self.name)

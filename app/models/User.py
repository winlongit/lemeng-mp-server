from app.dbengines import db
from Picture import Picture
import datetime


# 用户管理model
class User(db.Document):
    xcc_openid = db.StringField(verbose_name='微信对应的小程序id')
    tel = db.StringField(verbose_name='手机')
    name = db.StringField(verbose_name='姓名')
    sex = db.StringField(verbose_name='性别')
    id_card = db.StringField(verbose_name='身份证号码')
    province = db.StringField(verbose_name='省')
    city = db.StringField(verbose_name='市')
    area = db.StringField(verbose_name='区')
    address = db.StringField(verbose_name='地址')
    avatar = db.ReferenceField(Picture, verbose='头像')
    create_time = db.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')
    update_time = db.DateTimeField(default=datetime.datetime.now, verbose_name='更新时间')

    def __unicode__(self):
        return str(self.xcc_openid)

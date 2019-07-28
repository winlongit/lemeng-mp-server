from app.dbengines import db
from Picture import Picture
import datetime


# 用户管理model
class EFLUser(db.Document):
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

    height = db.StringField(verbose_name='身高')
    weight = db.StringField(verbose_name='体重多少？（斤/公斤)')
    age = db.StringField(verbose_name='年龄')
    big_target = db.StringField(verbose_name='健康管理目标')
    detail_target = db.StringField(verbose_name='减肥目标')
    data = db.StringField(verbose_name='体检的报告')
    more = db.StringField(verbose_name='多了解下您的状况')
    type = db.StringField(verbose_name='肥胖种类')  # { 1.单纯性肥胖/ 2.遗传性肥胖 / 3.继发性肥胖}
    time = db.StringField(verbose_name='每周有计划的运动时间大概几分钟')
    activity = db.StringField(verbose_name='喜欢什么种类的运动')
    taocan = db.StringField(verbose_name='建 议您采用“乐盟基础个性化健康管理”套餐')
    shop = db.StringField(verbose_name='乐盟商城有很多适合您的健康产品与服务')

    informed = db.StringField(verbose_name='是否结束收集信息')

    def __unicode__(self):
        return str(self.xcc_openid)

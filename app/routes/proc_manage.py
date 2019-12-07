from flask import request, Blueprint, jsonify
from app.models import Product,OnePicture

from app import app

config = app.config
bp = Blueprint('proc_manage', __name__, url_prefix="/shop/proc_manage")


@bp.route("/add_proc", methods=["POST"])
def add_proc():
    # 数据格式
    # dict_items([('name', '神鼎飞丹砂'), ('yuan', 11), ('cent', 11), ('type', '健康食品'), ('category', '五谷杂粮'),
    #             ('specification', [{'value': '胜多负少的', 'canDelete': False}]), ('swiperImages', [
    #         {'order': 1, 'pic_id': '5daec15918e7c1e59a26128c', 'name': 'timg.jpg'},
    #         {'order': 2, 'pic_id': '5daec15918e7c1e59a261288', 'name': 'u=1975038247,3581492848&fm=26&gp=0.jpg'}]), (
    #             'descImages', [{'order': 1, 'pic_id': '5daec15d18e7c1e59a261291',
    #                             'name': 'u=1975038247,3581492848&fm=26&gp=0.jpg'}])])
    json_data = request.get_json()  # 返回的 json_data 是一个 dict
    print(json_data.items())
    print(json_data.keys())
    proc = Product()
    proc.name = json_data["name"]
    proc.description = json_data["description"]
    proc.price = int(json_data["yuan"]) * 100 + int(json_data["cent"])
    proc.type = json_data["type"]
    proc.category = json_data["category"]
    proc.specification = [spec["value"] for spec in json_data["specification"]]
    proc.list_swipers = [OnePicture(order=swiper["order"], pic_id=swiper["pic_id"]) for swiper in json_data["swiperImages"]]
    proc.list_desc = [OnePicture(order=desc["order"], pic_id=desc["pic_id"]) for desc in json_data["descImages"]]
    print(json_data.get("name"))
    print(json_data.get("swiperImages", "haha"))
    print(proc.to_mongo())
    rs = proc.save()
    # proc = Product(name=json_data["name"])
    return jsonify(rs)

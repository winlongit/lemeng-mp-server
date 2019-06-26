import time
from datetime import datetime

from flask import request, session, render_template, Blueprint, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from app import app

config = app.config
bp = Blueprint('task', __name__, url_prefix="/task")


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(4, 20)])


@bp.route("/")
def task_list():
    return 'Hello World2222222!'


@bp.route("/getJson")
def get_json():
    form = MyForm()
    print(form.data)
    return jsonify({"name": "sb", "age": 2})


@bp.route("/getTask")
def get_task():
    print("getTask")
    return jsonify({"name": "sb", "age": 2})

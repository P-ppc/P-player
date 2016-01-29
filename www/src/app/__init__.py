#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


from app import views, models

@app.template_filter('danmu_time')
def danmu_time(time):
    danmu_time = str()
    seconds = int(time) / 10
    mins = seconds / 60
    danmu_time += '0' + str(mins) if mins < 10 else str(mins)
    secs = seconds % 60
    danmu_time += ':'
    danmu_time += '0' + str(secs) if secs < 10 else str(secs)
    return danmu_time

@app.template_filter('danmu_datetime')
def danmu_datetime(danmu_time):
    danmu_time = str(danmu_time)
    if danmu_time != None and danmu_time != '':
        return danmu_time[6: -3]
    else:
        return ''

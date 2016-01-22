#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time, StringIO
from datetime import datetime
import json

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, db, lm
from models import User, Video, Danmu, Comment
from config import MEDIA_DIR
from utils import toDict, get_logging

'''
init logging.
'''
logging = get_logging()


@app.route('/', methods = ['GET'])
def index():
    videos = Video.query.all()
    return render_template('index.html', videos = videos) 
    
# for play

@app.route('/<video_id>', methods = ['GET'])
def play(video_id):
    video = Video.query.get_or_404(video_id)
    return render_template('play.html', video = video) 

@app.route('/<video_id>/getDanmu')
def get_danmu(video_id):
    #danmu1 = '{text: "弹幕", color: "white", size: "1", position: "0", time: "2"}'
    danmu_list = list()
    danmus = Danmu.query.order_by(Danmu.time).filter_by(video_id = video_id).all()
    for danmu in danmus:
        danmu_text = '{text: "%s", color: "%s", size: "%s", position: "%s", time: "%s"}' % (danmu.text, danmu.color, danmu.size, danmu.position, danmu.time)
        danmu_list.append(danmu_text)
    return json.dumps(danmu_list)

@app.route('/<video_id>/postDanmu', methods = ['GET', 'POST'])
def post_danmu(video_id):
    danmu_txt = request.form.get('danmu', None)
    if danmu_txt is None:
        logging.debug('no danmu txt')
        return 'no txt'
    danmu_txt = danmu_txt.encode('utf-8')
    logging.debug(danmu_txt)
    video = Video.query.get(video_id)
    danmu_Dict = toDict(json.loads(danmu_txt))
    danmu = Danmu(text = danmu_Dict.text,
            color = danmu_Dict.color,
            position = danmu_Dict.position,
            size = danmu_Dict.size,
            time = danmu_Dict.time,
            video = video)
    db.session.add(danmu)
    db.session.commit()
    logging.debug('danmu add OK')
    return 'danmu add OK'

# for user

# for comment

# for post



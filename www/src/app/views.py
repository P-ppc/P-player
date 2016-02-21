#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time, StringIO
from datetime import datetime
import json

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, db, lm
from models import User, Video, Danmu, Comment, Classify, Collection, PlayRecord
from config import MEDIA_DIR 
from utils import toDict, get_logging
from forms import LoginForm, RegisterForm, ChangePasswordForm

'''
init logging.
'''
logging = get_logging()

@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
def index():
    classifys = Classify.query.order_by(Classify.sort).all()
    return render_template('index.html', classifys = classifys) 
    
# for play

@app.route('/<video_id>', methods = ['GET'])
def play(video_id):
    video = Video.query.get_or_404(video_id)
    record = PlayRecord(
            play_time = datetime.now(),
            video = video,
            classify = video.classify)
    db.session.add(record)
    db.session.commit()
    return render_template('play.html', video = video) 

@app.route('/<video_id>/getDanmu')
def get_danmu(video_id):
    danmu_list = list()
    danmus = Danmu.query.order_by(Danmu.time).filter_by(video_id = video_id).all()
    for danmu in danmus:
        danmu_text = '{text: "%s", color: "%s", size: "%s", position: "%s", time: "%s"}' % (danmu.text, danmu.color, danmu.size, danmu.position, danmu.time)
        danmu_list.append(danmu_text)
    return json.dumps(danmu_list)

@app.route('/<video_id>/postDanmu', methods = ['POST'])
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
            video = video,
            danmu_time = datetime.now(),
            user = g.user)
    db.session.add(danmu)
    db.session.commit()
    logging.debug('danmu add OK')
    return 'danmu add OK'

# for user
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user) 
        return redirect(request.args.get('next') or url_for('index'))
    
    return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form = form)

@app.route('/change_password', methods = ['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(g.user)
    logging.debug(form.validate_on_submit())
    logging.debug(form.errors)
    if form.validate_on_submit():
        g.user.password = form.new_password.data
        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('change_password.html', form = form)

@app.route('/change_profile', methods = ['GET', 'POST'])
@login_required
def change_profile():
    if request.method == 'POST':
        avator_type = ('.jpeg', '.png', '.jpg')
        f = request.files.get('avator', None)
        sign = request.form.get('sign', '')
        avator_path = str()
        if f != None and f.filename.endswith(avator_type):
            avator_path = str(int(time.time())) + '.' + f.filename.split('.')[-1] 
            f.save(MEDIA_DIR + '/' + avator_path)
        g.user.sign = sign
        g.user.avator = avator_path
        db.session.add(g.user)
        db.session.commit() 
        return redirect(url_for('index'))
    return render_template('change_profile.html')

# for comment
@app.route('/<video_id>/add_comment', methods = ['POST'])
@login_required
def add_comment(video_id):
    video = Video.query.get_or_404(video_id)
    sort = Comment.query.filter_by(video_id = video_id).count() + 1
    content = request.form.get('content', '')
    comment = Comment(content = content, 
                      sort = sort,
                      video = video,
                      user = g.user)
    db.session.add(comment)
    db.session.commit()
    # return json.dumps({'result': 'success'})
    return redirect(url_for('play', video_id = video_id))

# for post

# for upload video

@app.route('/file_upload')
@login_required
def file_upload():
    return render_template('video_upload.html')

@app.route('/file_stream', methods = ['POST'])
@login_required
def flie_stream():
    '''
    Just save the video.
    '''
    f = request.files.get('file[]', None)
    logging.debug(f.filename)
    try:
        if f is not None and f.filename.endswith('.mp4'):
            path = str(int(time.time())) + '.mp4'
            f.save(MEDIA_DIR + '/' + path)
        return json.dumps({'result': 'success', 'path': path })
    except:
        return json.dumps({'result': 'fail'})

@app.route('/save_video', methods = ['POST'])
@login_required
def save_video():
    '''
    Save the title, path, cover, upload_time, collection_sort ... in db.
    '''
    title = request.form.get('title', None)
    path = request.form.get('video', None)
    cover = request.files.get('cover', None)
    cover_type = ('.jpeg', '.png', '.jpg')
    if cover is not None and cover.filename.endswith(cover_type):
        cover_path = str(int(time.time())) + '.' +cover.filename.split('.')[-1]
        cover.save(MEDIA_DIR + '/' + cover_path)
    else:
        cover_path = None
    upload_time = datetime.now()
    classify = Classify.query.all()[0]
    video = Video(
                title = title,
                path = path,
                cover = cover_path,
                upload_time = upload_time,
                classify = classify,
                user = g.user)
    db.session.add(video)
    db.session.commit()
    #return json.dumps({'result': 'success'})
    return redirect(url_for('index'))

@app.route('/test')
def test():
    return render_template('video_upload.html')

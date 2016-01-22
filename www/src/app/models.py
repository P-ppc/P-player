#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Models for user, video, comment, danmu.
'''

from app import db
from app import app

class User(db.Model):
    '''
    Model for user.
    '''
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(64))

    videos = db.relationship('Video', backref = 'user', lazy = 'dynamic')
    danmus = db.relationship('Danmu', backref = 'user', lazy = 'dynamic')
    comments = db.relationship('Comment', backref = 'user', lazy = 'dynamic')

class Video(db.Model):
    '''
    Model for video.
    '''
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))               # 标题
    path = db.Column(db.String(140))                # 路径
    no = db.Column(db.String(64), unique = True)    # 编号  如: av110

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    danmus = db.relationship('Danmu', backref = 'video', lazy = 'dynamic')
    comments = db.relationship('Comment', backref = 'video', lazy = 'dynamic')

class Danmu(db.Model):
    '''
    Model for danmu.
    '''
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text)           # 文本
    color = db.Column(db.String(10))    # 颜色
    position = db.Column(db.String(10)) # 位置 （0为滚动，1为顶部，2为底部）
    size = db.Column(db.String(10))     # 文字大小 （0为小字，1为大字）
    time = db.Column(db.String(10))     # 弹幕出现的时间 （单位为十分之一秒）

    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)        # 评论内容
    
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  

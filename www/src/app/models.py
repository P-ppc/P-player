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
    collections = db.relationship('Collection', backref = 'user', lazy = 'dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

class Video(db.Model):
    '''
    Model for video.
    '''
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))               # 标题
    path = db.Column(db.String(140))                # 路径
    no = db.Column(db.String(64), unique = True)    # 编号  如: av110
    cover = db.Column(db.String(64))                # 封面  大小为 160 X 100 最合适
    upload_time = db.Column(db.DateTime)            # 上传时间
    collection_sort = db.Column(db.Integer)         # 在合集中的排序 

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    classify_id = db.Column(db.Integer, db.ForeignKey('classify.id'))

    danmus = db.relationship('Danmu', backref = 'video', lazy = 'dynamic')
    comments = db.relationship('Comment', backref = 'video', lazy = 'dynamic')
    play_records = db.relationship('PlayRecord', backref = 'video', lazy = 'dynamic')

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'path': self.path,
            'no': self.no,
            'cover': self.cover_path
        }
    
    @property
    def cover_path(self):
        if self.cover is None or self.cover == '':
            return 'nopic.jpg'
        else:
            return self.cover

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
    danmu_time = db.Column(db.DateTime) # 发送弹幕的时间 

    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)        # 评论内容
    sort = db.Column(db.Integer)        # 评论楼层
    comment_time = db.Column(db.DateTime)   # 评论时间
     
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  

class Classify(db.Model):
    '''
    Model for Classify. 分类.
    '''
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))     # 分类名称
    sort = db.Column(db.Integer)        # 在分类的排行

    videos = db.relationship('Video', backref = 'classify', lazy = 'dynamic')
    play_records = db.relationship('PlayRecord', backref = 'classify', lazy = 'dynamic')
    collections = db.relationship('Collection', backref = 'classify', lazy = 'dynamic')

    def rank_list(self):
        # 获取播放量前10的视频
        rank_list = db.session.query(Video).from_statement(
              "select video.*, record.count from video"
            + " left join (select count(video_id) count, video_id from play_record group by video_id) record on video.id = record.video_id"
            + " where video.classify_id = :classify_id"
            + " order by record.count desc"
            + " limit 0, 10"
            ).params(classify_id = self.id).all()
        return rank_list

class Collection(db.Model):
    '''
    Model for Collection. 合集.
    '''
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))     # 合集名称
    create_time = db.Column(db.DateTime)# 创建时间

    classify_id = db.Column(db.Integer, db.ForeignKey('classify.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    videos = db.relationship('Video', backref = 'collection', lazy = 'dynamic')

class PlayRecord(db.Model):
    '''
    Model for PlayRecord. 播放记录.
    '''
    id = db.Column(db.Integer, primary_key = True)
    play_time = db.Column(db.DateTime)

    classify_id = db.Column(db.Integer, db.ForeignKey('classify.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))

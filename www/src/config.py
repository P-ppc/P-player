# -*- coding: utf-8 -*-
import os

wwwdir = os.path.abspath(os.path.dirname(__file__)) 

'''
Flask config.
'''
SQLALCHEMY_DATABASE_URI = 'mysql://www-data:www-data@localhost/player'
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLE = True
SECRET_KEY = 'you-will-never-guess'

'''
media dir.
'''
MEDIA_DIR = os.path.join(wwwdir, '../media')

'''
logging file.
'''
LOGGING_FILE = os.path.join(wwwdir, '../../log/run.log')

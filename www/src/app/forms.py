# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from app.models import User

class LoginForm(Form):
    username = StringField('username', validators = [DataRequired()])
    password = StringField('password', validators = [DataRequired()])

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(username = self.username.data, password = self.password.data).first()
        if user is not None:
            self.user = user
            return True
        self.password.errors.append(u'用户名或密码错误！')
        return False

class RegisterForm(Form):
    username = StringField('username', validators = [DataRequired()])
    password = StringField('password', validators = [DataRequired()])
    password_repeat = StringField('password_repeat', validators = [DataRequired()])

    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(username = self.username.data).first()
        if user is not None:
            self.username.errors.append(u'该用户名已被使用！')
            return False
        if self.password.data != self.password_repeat.data:
            self.password_repeat.errors.append(u'两次密码输入不一致！')
            return False
        return True

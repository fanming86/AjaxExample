#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('config')
# flatpages = FlatPages(app)
boottstrap = Bootstrap(app)


#初始化数据库
db = SQLAlchemy(app)

# 初始化flask-Login
lm = LoginManager()
lm.session_protection = 'strong'     # 记录客户端ip，用户代理信息，发现异动，登出用户,可以设置不同等级None,'basic','strong'
lm.login_view = 'login'     #设置登陆页面，为认证的登陆转到此页面
lm.init_app(app)

# csrf = CsrfProtect()
# csrf.init_app(app)


from app import views,models

from user import user
app.register_blueprint(user)
#coding:utf-8

from app import db

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import json,uuid

PROFILE_FILE = "profiles.json"


class User(db.Model):
    __tablename__ = "du_user"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    phone = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), unique=True)
    create_time = db.Column(unique=True)

    def __init__(self, username, phone, password, create_time):
        self.username = username
        self.phone = phone
        self.password = password
        self.create_time = create_time

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        return '<User %r>' % (self.username)
    '''
is_authenticated方法是一个误导性的名字的方法，通常这个方法应该返回True，除非对象代表一个由于某种原因没有被认证的用户。

is_active方法应该为用户返回True除非用户不是激活的，例如，他们已经被禁了。

is_anonymous方法应该为那些不被获准登录的用户返回True。

最后，get_id方法为用户返回唯一的unicode标识符。我们用数据库层生成唯一的id。
    '''

class Duty(db.Model):
    __tablename__ = "du_duty"
    duty_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(64), unique=True)
    status = db.Column(db.Integer, unique=True)
    is_show = db.Column(db.Integer, unique=True)
    create_time = db.Column(db.Integer, unique=True)

    def __init__(self, category_id, user_id, title, status, is_show, create_time):
        self.category_id = category_id
        self.user_id = user_id
        self.title = title
        self.status = status
        self.is_show = is_show
        self.create_time = create_time

class Category(db.Model):
    __tablename__ = "du_category"
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Article(db.Model):
    __tablename__ = "article"
    article_id = db.Column(db.String(5), primary_key=True,)
    article_name = db.Column(db.String(64), unique=True)
    article_time = db.Column(db.DateTime)
    article_click = db.Column(db.Integer, unique=True)
    sort_article_id = db.Column(db.Integer,unique=True)
    user_id = db.Column(db.Integer, unique=True)
    article_type = db.Column(db.Integer, unique=True)
    article_content = db.Column(db.Text, unique=True)
    article_up = db.Column(db.Integer, unique=True)
    article_support = db.Column(db.Integer, unique=True)


    def __init__(self,article_id,article_name,article_time,article_click,sort_article_id,user_id,article_type,article_content,article_up,article_support):
        self.article_id =article_id
        self.article_name =article_name
        self.article_time =article_time
        self.article_click =article_click
        self.sort_article_id =sort_article_id
        self.user_id =user_id
        self.article_type =article_type
        # self.article_content =article_content
        self.article_up =article_up
        self.article_support = article_support
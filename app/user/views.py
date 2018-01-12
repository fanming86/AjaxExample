#coding:utf-8

from flask import render_template, redirect, request, url_for, flash
from . import user
###从本级目录中导入auth蓝本
from ..models import Article
###从上级目录中的models.py导入User模型
from app.forms import LoginForm
#从本级目录中的forms.py中导入LoginForm类




@user.route('/blog',methods = ['POST','GET'])
def blog():
    article = Article.query.all()
    return render_template("BlogIndex.html",article=article)


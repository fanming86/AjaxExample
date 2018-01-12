#coding:utf-8
from flask_wtf import FlaskForm###从Flask-WTF扩展导入Form基类
from wtforms import IntegerField ,StringField, PasswordField, BooleanField,TextField,TextAreaField, SubmitField###从WTForms包中导入字段类
from wtforms.validators import Required,Length,Email, DataRequired###从WTForms导入验证函数

class LoginForm(FlaskForm):
    phone = IntegerField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)
    submit = SubmitField('LOGIN')


class Register(FlaskForm):
    phone = IntegerField('Phone', validators=[DataRequired()])
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repassword = PasswordField('RePassword', validators=[DataRequired()])
    submit = SubmitField('REGISTER')

class AboutMeForm(FlaskForm):
    describe = TextAreaField('about me', validators=[
        Required(), Length(max=140)])
    submit = SubmitField('YES!')


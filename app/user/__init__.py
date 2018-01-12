# coding:utf-8

from flask import Blueprint, render_template


user = Blueprint('user', __name__)

from . import views


#
# Base = declarative_base()
# engine = create_engine('mysql+mysqlconnector://root:1234@localhost/dutylist')
# DBSession = sessionmaker(bind=engine)
# db = DBSession()
#
#
# class User(Base):
#     __tablename__ = "du_user"
#     user_id = Column(Integer, primary_key=True)
#     username = Column(String(64), unique=True)
#     phone = Column(String(64), unique=True)
#     password = Column(String(64), unique=True)
#     create_time = Column(unique=True)
#
#     def __init__(self, username, phone, password, create_time):
#         self.username = username
#         self.phone = phone
#         self.password = password
#         self.create_time = create_time
#
#     def __repr__(self):
#         return self.username
#
#
# @user.route('/hello')
# def hello():
#     return render_template('test.html')
#
#
# @user.route('/login', methods=['GET', 'POST'])
# def login():
#     myname = None
#     if request.method == "POST":
#         phone = request.form['phone']  # 获取用户输入的表单phone
#         password = request.form['password']
#         if phone and password:
#             try:
#                 user = db.query(User).filter(User.phone == phone).one()
#             except:
#                 flash( 'phone not exist!')
#                 return redirect(url_for('user.login1'))
#             else:
#                 if user.password == password:
#                     flash( 'login secusse!')
#                     return redirect(url_for('my_duty'))
#                 else:
#                     flash( "password error!!!")
#                     return redirect(url_for('user.login1'))
#         else:
#             flash( 'phone or password is none!')
#             return redirect(url_for('user.login1'))
#     flash('login error! please login again！')
#     return render_template('login1.html', myname=myname)
#
#
# # @user.route('/logout')
# # def logout():
# #     session.pop('user_id', None)
# #     session.pop('username', None)
# #     return redirect(url_for('index'))
#
#
# @user.route('/register', methods=['GET', 'POST'])
# def register():
#     myname = None
#     if request.method == "POST":
#         username = request.form['username']
#         phone = request.form['phone']
#         password = request.form['password']
#         repassword = request.form['repassword']
#
#         if username or phone or password or repassword:
#             if password != repassword:
#                 flash('Password and Confirm Password not same')
#                 return redirect(url_for('register1'))
#             try:
#                 res = db.query(User).filter(User.phone == phone).one()
#             except:
#                 data = User(username, phone, password, time.time())
#                 db.add(data)
#                 db.commit()
#                 if data.user_id:
#                     flash('register successfully! please login')
#                     return redirect(url_for('user.login1'))
#                 else:
#                     flash('register error!')
#                     return redirect(url_for('user.register1'))
#             if res:
#                 flash('phone is be register')
#                 return redirect(url_for('user.register1'))
#         else:
#             flash('field can not be empty')
#             return redirect(url_for('user.register1'))
#     else:
#         flash("register error!!! plase register afain")
#         return render_template('register.html', myname=myname)
#
#
# @user.route('/login1')
# def login1():
#     return render_template("login1.html")
#
#
# @user.route("/register1")
# def register1():
#     return render_template("register.html")
#
# @user.route('/logout')
# ###退出路由
# @login_required
# ###用户要求已经登录
# def logout():
#     logout_user()
#     ###登出用户，这个视图函数调用logout_user()函数，删除并重设用户会话。
#     flash('You have been logged out.')
#     ###显示flash消息
#     return redirect(url_for('main.index'))
#     ###重定向到首页


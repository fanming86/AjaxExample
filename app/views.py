# coding:utf-8

from flask import render_template,url_for,request,flash,redirect,session
from flask_login import login_user, logout_user, current_user, login_required
import time
import sys,json
from app import app,db,lm
from models import User,Category,Duty,Article
from .forms import  LoginForm,Register

reload(sys)
sys.setdefaultencoding('utf8')




# 这个callback函数用于reload User object，根据session中存储的user id
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/product/list")
def product_list():
    return render_template("productList.html")
tmp_time = 0
@app.route('/data')
def data():
    global tmp_time
    if tmp_time>0:
        sql = 'select * from memory where time>%s' % (tmp_time/1000)
    else:
        sql = 'select * from memory'
    db.session.execute(sql)
    arr = []
    for i in db.session.execute(sql).fetchall():
        arr.append([i[1]*1000,i[0]])
    if len(arr)>0:
        tmp_time = arr[-1][0]
    return json.dumps(arr)



@app.route("/user/list")
def user_list():
    form = Register()
    return render_template("userList.html",form=form)

@app.route("/record/list/<int:user_id>",methods=["POST","GET"])
def record_list(user_id):
    article = User.query.filter_by(user_id=user_id).first()
    return render_template("recordList.html",article=article)

@app.route('/record/log')
def log():
    return render_template('log.html')



@app.route('/my_duty')
def my_duty():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        myname = session['username']
        if request.method == 'GET' and request.args.get('category_id'):
            category_id = request.args.get('category_id')
            sql = 'select t1.*,t2.name from du_duty as t1  left join du_category as t2 on t2.category_id = t1.category_id where t1.user_id = %s  and t1.category_id = %s' % (
            session['user_id'], category_id)
        else:
            sql = 'select t1.*,t2.name from du_duty as t1  left join du_category as t2 on t2.category_id = t1.category_id where user_id = %s' % \
                  session['user_id']
        duty_list = db.session.execute(sql).fetchall()
        category_list = Category.query.order_by(Category.category_id).all()
        return render_template('my_duty.html', duty_list=duty_list, category_list=category_list,myname=myname)

# 保护路由，未认证的用户请求会被拦截，转往登陆页面
@app.route('/my_duty')
@login_required
def main():
    flash("Please login first!")
    return render_template('my_duty.html',username=current_user.username)

@app.route('/add_duty',methods=['GET','POST'])
def add_duty():
	if 'user_id' not in session:
		return redirect(url_for('login'))
	else:
		myname = session['username']
		if request.method == "POST":
			title = request.form['title']
			print title
			category_id = request.form['name']
			is_show = request.form['is_show']
			status = request.form['status']
			if title and category_id:
				data = Duty(category_id,session['user_id'],title,status,is_show,time.time())
				res = db.session.add(data)
				db.session.commit()
				print data.duty_id
				if data.duty_id:
					flash('add successfully! ')
					return redirect(url_for('my_duty'))
				else:
					flash('register error!')
					return redirect(url_for('add_duty'))
			else:
				flash('field can not be empty')
				return redirect(url_for('add_duty'))
		else:
			category_list = Category.query.order_by(Category.category_id).all()
			return render_template('add_duty.html',category_list = category_list)

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        myname = session['username']
        if request.method == 'POST':
            name = request.form['name']
            if name:
                res = Category.query.filter_by(name=name).first()
                if res:
                    flash('catgory is be here')
                    return redirect(url_for('add_category'))
                else:
                    data = Category(name)
                    res = db.session.add(data)
                    db.session.commit()
                    return redirect(url_for('my_duty'))
            else:
                flash('name not be None!')
                return render_template('add_category.html')

        return render_template('add_category.html', username=session['username'], myname=myname)

@app.route('/logout')
###退出路由
@login_required
###用户要求已经登录
def logout():
    logout_user()
    ###登出用户，这个视图函数调用logout_user()函数，删除并重设用户会话。
    flash(message='You have been logged out.',category='info')
    ###显示flash消息
    return redirect(url_for('user_list'))
    ###重定向到首页

@app.route('/login', methods=['GET', 'POST'])
###当请求为GET时，直接渲染模板，当请求是POST提交时，验证表格数据，然后尝试登入用户。
def login():
    form = LoginForm()
    if request.method == 'POST':
        phone1 = request.form.get('phone')
        passwd = request.form.get('password')
        if phone1 and passwd:
            user = User.query.filter_by(phone=phone1).first()
            if user:
                if user.password == passwd:
                    login_user(user)
                    session['user_id'] = user.user_id
                    session['username'] = user.username
                    flash(message='Login success!',category='success')
                    return redirect(url_for("my_duty"))
                else:
                    flash(message='password error',category='danger')
                    return render_template('login.html', form=form)
            else:
                flash(message='phone not exsit',category='danger')
                return render_template('login.html', form=form)
        else:
            flash('The username and password can not be empty')
            return render_template('login.html', form=form)
    elif request.method == 'GET':
        return render_template('login.html', form=form)


@app.route('/register' ,methods=["GET","POST"])
def register():
    form = Register()
    if request.method=='GET':
        return render_template('register.html',form=form)
    elif request.method=='POST':
        if form.validate_on_submit():
            user = User.query.filter_by(phone=form.phone.data).first()
            if user:
                flash(message='Phone number has been registered',category='danger')
                return render_template('register.html',form=form)
            else:
                if form.password.data == form.repassword.data:
                    add_user = User(form.username.data,form.phone.data,form.password.data,time.time())
                    db.session.add(add_user)
                    db.session.commit()
                    flash(message='Register successfully, please login',category='success')
                    return redirect('/login')
                else:
                    flash(message='The passwords entered twice are not the same',category='danger')
                    return render_template('register.html',form=form)
        else:
            return 'None'



@app.route('/test',methods = ['POST','GET'])
def test():
    if current_user.is_authenticated:
        return redirect('index')
    # 注册验证
    form = LoginForm()
    if form.validate_on_submit():
        print form.password
        # user = User.login_check(request.form.get('phone'))
        # if user:
        #     login_user(user)
        #     user.last_seen = datetime.datetime.now()
        #
        #     try:
        #         db.session.add(user)
        #         db.session.commit()
        #     except:
        #         flash("The Database error!")
        #         return redirect('user.login')
        #
        #     flash('Your name: ' + request.form.get('phone'))
        #     flash('remember me? ' + str(request.form.get('remember_me')))
        #     return redirect(url_for("index", user_id=current_user.id))
        # else:
        #     flash('Login failed, Your name is not exist!')
        #     return redirect('user.login')

    return render_template(
        "test.html",
        title="Sign In",
        form=form)














@app.errorhandler(404)
def page_not_found(e):
	myname = None
	if 'user_id' in session:
		myname = session['username']
	return render_template('404.html',myname=myname), 404

@app.errorhandler(500)
def internal_server_error(e):
	myname = None
	if 'user_id' in session:
		myname = session['username']
	return render_template('500.html',myname=myname), 500


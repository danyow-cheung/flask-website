import functools
import sys
from flask import (
        Blueprint,flash,g,redirect,render_template,request,session,url_for)

from werkzeug.security import check_password_hash,generate_password_hash
from werkzeug.utils import secure_filename
import numpy as np

from .sqlitedb import connect_db
from functools import wraps 

bp = Blueprint('user',__name__,url_prefix='/user')


def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if g.user is None:
            return redirect(url_for('user.login',next = request.url))
        return f(*args,**kwargs)
    return decorated_function

    
@bp.route('/register',methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = connect_db()
        error = None
        if not username:
            error ='用户名不能为空'
        elif not password:
            error = '密码不能为空'

        elif db.execute(
               'SELECT id FROM user WHERE username =?',(username,)
               ).fetchone() is not None:
            error = 'user{}already registered'.format(username)

        if error is None:
            db.execute(
                    'INSERT INTO user(username,password) VALUES(?,?)',
                    (username,generate_password_hash(password))
                    )
            db.commit()
            return redirect(url_for('user.login'))

        flash(error)

    return render_template('register.html')
        
@bp.route('/login',methods=('GET','POST'))

def login():
    if request.method =="POST":
        username = request.form['username']
        password=request.form['password']
        db = connect_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username=?',(username,)
            ).fetchone()

        if user is None:
            error = "用户名不正确"
        elif not check_password_hash(user['password'],password):
            error="密码不正确"
        if error is None:
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('index'))

        flash(error)
    return render_template('login.html')
     
@bp.route("/create,",methods=("GET","POST"))
def create():
    if request.method=="POST":
        score = request.form['score']
        error = None

        if not score:
            error = "成绩不能为空"

        if error is not None:
            flash(error)
        
        else:
            db = connect_db()
            db.execute(
                'INSERT INTO score(score) VALUES(?)',[score]
            )
            db.commit()
            return redirect(url_for("score.index"))

    return render_template("create.html")


@bp.route("/login",methods=("GET","POST"))
@bp.before_app_request
def load_logged_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = connect_db().execute(
            'SELECT * FROM user where id = ?',(user_id,)
        ).fetchone()


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))



   
@bp.route('/index1')
def index():
    flash('超时错误',category="error")
    flash('普通错误',category='info')
    return 'ssdsdsdfsd'

@bp.route('/error')
def error():
    data = get_flashed_messages(with_categories=True,category_filter=("error","info"))
    data1 = get_flashed_messages(with_categories=True, category_filter=("error", "info"))
    print("data1",data1)
    print("data",data)
    return "错误信息"

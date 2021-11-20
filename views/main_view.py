'''
view는 우리 눈에 보이는 부분을 관리합니다.

지난 시간에 작업했을 때는 view를 여러 파일로 분리하지 않았는데, 상황에 따라 파일을 분리할 수 있습니다.
그러면 어떻게 관리하냐고요?

어차피 각 파일마다 별도의 Blueprint를 만들테니, __init__.py에서 전부 import 하고
각각 다 register_blueprint를 활용해서 이어줍니다.

추가로, 코드를 보다보면 query를 사용한 것이 많은데, 이를 활용하면 SQL 구문을 직접 사용하지 않고
ORM을 통해 간접적으로 db에 작업 명령을 내릴 수 있습니다.
'''

from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.models import *
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def home():
    book_list = lib_books.query.order_by(lib_books.book_id.asc())
    return render_template('main.html', book_list=book_list)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'GET':
        return render_template('register.html')
        
    elif request.method == 'POST':
        # 회원가입 과정을 거쳐야겠다!
        # 만약에 같은 아이디가 있으면 어떡해?
        user = lib_users.query.filter_by(user_email=request.form['user_email']).first()
        if not user:
            user_pw = generate_password_hash(request.form['user_pw'])

            user = lib_users(user_email=request.form['user_email'], user_pw=user_pw, user_name=request.form['user_name'])
        
            db.session.add(user)
            db.session.commit()

            flash("회원가입이 완료되었습니다.")
            return redirect(url_for('main.home'))
        else:
            flash("이미 가입된 아이디입니다.")
            return redirect(url_for('main.register'))

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        user_email = request.form['user_email']
        user_pw    = request.form['user_pw']

        user_data = lib_users.query.filter_by(user_email=user_email).first()

        if not user_data:
            flash("없는 아이디입니다.")
            return redirect(url_for('main.login'))

        elif not check_password_hash(user_data.user_pw, user_pw):
            flash("비밀번호가 틀렸습니다.")
            return redirect(url_for('main.login'))

        else:
            session.clear()
            session['user_email']   = user_email
            session['user_name']    = user_data.user_name

            flash(f"{user_data.user_name}님, 환영합니다!")
            return redirect(url_for('main.home'))
            
# @bp.route('/status')
# def status():


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))

@bp.route('/check_info')
def info():
    print("hello")
    return render_template('check_info.html')

@bp.route('/check_out')
def out():
    return render_template('check_out.html')
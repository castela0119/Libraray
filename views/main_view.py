from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.models import *
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sql

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def home():
    book_list = lib_books.query.order_by(lib_books.book_id.asc())
    status_info = lib_status.query.filter_by(book_id=lib_status.book_id).first()

    return render_template('main.html', book_list=book_list, status_info=status_info)

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


@bp.route('/rent/<int:book_id>', methods=('POST', ))
def rent(book_id):
    book_info = lib_books.query.filter_by(book_id=book_id).first()
    review_info = lib_reviews.query.filter_by(book_id=book_id).first()

    if 'user_email' not in session:
        flash('권한이 없습니다. 로그인 해주세요.')
        return redirect(url_for('main.home'))

    else:
        if(book_info.book_counts == 0):
            flash(f"[{book_info.book_name}] 은 모두 대여된 상태입니다.")
        
        if(book_info.book_counts > 0):
            book_info.book_counts = book_info.book_counts - 1
            flash(f"[{book_info.book_name}] 이 대여 되었습니다.")

        id = book_info.book_id
        em = session['user_email']
        pc = book_info.img_path
        nm = book_info.book_name

        rating_sum, average = 0, 0

        if review_info:
            for review in review_info:
                rating_sum += review.rating
            average = rating_sum / len(review_info)

        avg = average

    with sql.connect('lib_rabbit.db') as con:
        cur = con.cursor()
        cur.execute('INSERT INTO lib_status(book_id, user_email, img_path, book_name, avg) VALUES (?, ?, ?, ?, ?)', (id, em, pc, nm, avg))
        con.commit()

    db.session.commit()

    
    return redirect(url_for('main.home'),)


# @bp.route('/rent/<int:book_id>', methods=('POST', ))
# def rent(book_id):
#     book_info = lib_books.query.filter_by(book_id=book_id).first()

#     if(book_info.book_counts > 0):
#         book_counts = book_info.book_counts - 1
#         book = lib_books(book_counts=book_counts)

#     db.session.add(book)
#     db.session.commit()

#     flash("대여가 완료되었습니다.")
#     return redirect(url_for('main.home'), book_counts=book_counts)


@bp.route('/info/<user_email>')
def rent_info(user_email):

    # book_list       = lib_books.query.order_by(lib_books.book_id.asc())
    # review_info     = lib_reviews.query.filter_by(book_id=book_id).first()
    status_info     = lib_status.query.filter_by(user_email=user_email).first()
    
    # db.session.query(lib_status, lib_books).filter(lib_status.user_email==user_email)
    
    if not status_info:
        flash("대여한 책이 없습니다.")
        return redirect(url_for('main.home'))
    else:
        
        return redirect(url_for('info.html'), status_info=status_info)
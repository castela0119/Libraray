from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import sqlite3 as sql

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def home():
    
    status_info = lib_status.query.filter_by(book_id=lib_status.book_id).first()

    page = request.args.get('page', type=int, default=1)  # 페이지

    page_list = lib_books.query.order_by(lib_books.book_id.asc())
    page_list = page_list.paginate(page, per_page=8)

    return render_template('main.html', status_info=status_info, page_list=page_list)

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
            
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))


@bp.route('/rent/<int:book_id>', methods=('POST', ))
def rent(book_id):

    if 'user_email' not in session:
        flash('권한이 없습니다. 로그인 해주세요.')
        return redirect(url_for('main.home'))

    else:
        user_email = session['user_email']
        status_info = lib_status.query.filter_by(book_id=book_id, user_email=user_email, now = 1).first()
        book_info = lib_books.query.filter_by(book_id=book_id).first()

        if(book_info.book_counts == 0):
            flash(f"[{book_info.book_name}] 은 모두 대여된 상태입니다.")

        elif(status_info is not None):
            flash(f"[{book_info.book_name}] 은 이미 대여된 상태입니다.")

        else:
            if(book_info.book_counts > 0):
                book_info.book_counts = book_info.book_counts - 1
                id = book_info.book_id
                em = session['user_email']
                status = lib_status(id, em)
                db.session.add(status)
                db.session.commit()
                flash(f"[{book_info.book_name}] 이 대여 되었습니다.")

        

        # rating_sum, average = 0, 0

        # if review_info:
        #     for review in review_info:
        #         rating_sum += review.rating
        #     average = rating_sum / len(review_info)

        # avg = average

    # with sql.connect('lib_rabbit.db') as con:
    #     cur = con.cursor()
    #     cur.execute('INSERT INTO lib_status(book_id,  book_name, now) VALUES (?, ?, ?, ?, ?, ?)', (id, em, pc, nm, avg, nw))
    #     con.commit()
    
    return redirect(url_for('main.home'),)

@bp.route('/info', methods=('GET', 'POST'))
def rent_info():
    
    user_email = session['user_email']

    status_info = db.session.query(lib_books, lib_status).join(
        lib_books, lib_books.book_id == lib_status.book_id
        ).filter(lib_status.user_email == user_email).all()

    now_info = lib_status.query.filter_by(user_email=user_email, now = 1).first()

    def get_score(book_id):
        items = db.session.query(lib_reviews).filter(lib_reviews.book_id == book_id).all()
        count = len(items)

        rating_sum = 0
        average = 0

        if items:
            for review in items:
                rating_sum += review.rating
            average = rating_sum / count
            average = round(average, 1)

        return average
    
    if not status_info:
        flash("대여한 책이 없습니다.")
        return redirect(url_for('main.home'))
    else:
        return render_template('info.html', get_score=get_score ,status_info=status_info, now_info=now_info)


@bp.route('/outbook/<int:book_id>', methods=['POST'])
def outbook(book_id):
    if request.method == 'POST': 
        book_info = lib_books.query.filter_by(book_id=book_id).first()
        status_info = lib_status.query.filter_by(book_id=book_id, now = 1).first()

        if(book_info.book_counts > 0):
                book_info.book_counts = book_info.book_counts + 1
                status_info.now = status_info.now - 1
                status_info.book_return = date.today()
                flash(f"[{book_info.book_name}] 이 반납 되었습니다.")

    db.session.commit()

    return redirect(url_for('main.rent_info'))

@bp.route('/history')
def history():
    user_email = session['user_email']

    status_info = db.session.query(lib_books, lib_status).join(
        lib_books, lib_books.book_id == lib_status.book_id
        ).filter(lib_status.user_email == user_email).all()

    def get_score(book_id):
        items = db.session.query(lib_reviews).filter(lib_reviews.book_id == book_id).all()
        count = len(items)

        rating_sum = 0
        average = 0

        if items:
            for review in items:
                rating_sum += review.rating
            average = rating_sum / count
            average = round(average, 1)

        return average

    return render_template('history.html', status_info=status_info, get_score=get_score)
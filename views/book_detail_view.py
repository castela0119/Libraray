from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.models import *
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('book_detail', __name__, url_prefix="/book")

# 일단 책 상세정보를 보여주는 페이지를 만들어야 한다.
@bp.route('/<int:book_id>')
def book_detail(book_id):

    # lib_books 의 정보를 다 가져와야 함
    # reveiw 의 정보도 다 가져와야 함 (review 테이블을 따로 만들어야 할지 고민해 볼 것)

    book_info = lib_books.query.filter_by(book_id=book_id).first()
    review_info = lib_reviews.query.filter_by(book_id=book_id).all()
    status_info = lib_status.query.filter_by(book_id=book_id).first()

    # 만약 book_info 에 없는 책을 주소창에 입력했을 경우

    if not book_info:
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))

    rating_sum, average = 0, 0

    if review_info:
        for review in review_info:
            rating_sum += review.rating
        average = rating_sum / len(review_info)

    return render_template("book_detail.html", avg=average, book_info=book_info, review_info=review_info, status_info=status_info)

# 리뷰를 써야하니깐, 리뷰를 작성할 수 있는 POST 를 받는 것을 만들어야 함.
@bp.route('/write_review/<int:book_id>', methods=('POST', ))
def create_review(book_id):

    # 권한 확인
    if 'user_email' not in session:
        flash('권한이 없습니다.')
        return redirect(url_for('main.home'))

    # 리뷰 작성에 필요한 데이터 -> book_id, content, star, user_email
    
    user_email = session['user_email']                # book_detail.html 에 들어가서 name="" 찾아보면 됨.
    review_content = request.form['review']
    review_rating = request.form['star']

    review = lib_reviews(user_email=user_email, book_id=book_id, rating=review_rating, content=review_content) # model.py 참고해서 작성해준 것.

    db.session.add(review)
    db.session.commit()

    flash('와! 리뷰! 아시는구나!')
    return redirect(url_for('book_detail.book_detail', book_id=book_id))

# 리뷰를 삭제할 수도 있음 -> 삭제 요청을 받는 걸 만들어야 함.
@bp.route('/delete_review/<int:book_id>')
def delete_review(book_id):
    review_id = request.args.get('review_id') # flask get 파라미터

    if 'user_email' not in session:
        flash("권한이 없습니다.")
        return redirect(url_for('main.home'))

    user_info   = lib_users.query.filter_by(user_email=session['user_email']).first()
    review_info = lib_reviews.query.filter_by(review_id=review_id).first()
    
    if not review_info:
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))

    if not user_info or review_info.user_email != session['user_email']:
        flash("권한이 없습니다.")
        return redirect(url_for('main.home'))

    db.session.delete(review_info)
    db.session.commit()

    flash("정상적으로 삭제 되었습니다.")

    book_info = lib_books.query.filter_by(book_id=review_info.book_id).first()
    return redirect(url_for("book_detail.book_detail", book_id=book_info.book_id))
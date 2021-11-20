from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.models import *
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('book_detail', __name__, url_prefix="/book")

# 일단 가게 정보를 보여주는 페이지를 만들어야 한다.
@bp.route('/<int:book_id>')
def book_detail(book_id):

    # lib_books 의 정보를 다 가져와야 함
    # reveiw 의 정보도 다 가져와야 함 (review 테이블을 따로 만들어야 할지 고민해 볼 것)

    book_info     = lib_books.query.filter_by(book_id=book_id).first()

    # 만약 book_info 에 없는 책을 주소창에 입력했을 경우

    if not book_info:
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))

    return render_template("book_detail.html", book_info=book_info)

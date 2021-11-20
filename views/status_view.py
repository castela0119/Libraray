from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.models import *
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('status', __name__, url_prefix="/status")

# 일단 가게 정보를 보여주는 페이지를 만들어야 한다.
@bp.route('/<int:user_no>')
def book_detail(user_no):

    # lib_books 의 정보를 다 가져와야 함
    # reveiw 의 정보도 다 가져와야 함 (review 테이블을 따로 만들어야 할지 고민해 볼 것)

    status_info     = lib_books.query.filter_by(user_no=user_no).first()

    # 만약 book_info 에 없는 책을 주소창에 입력했을 경우

    if not status_info:
        flash("잘못된 접근입니다.")
        return redirect(url_for('main.home'))

    return render_template("book_detail.html", status_info=status_info)

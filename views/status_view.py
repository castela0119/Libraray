from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.models import *
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('status', __name__, url_prefix="/rent")

@bp.route('/info/<int:book_id>')
def home(book_id):

    book_list       = lib_books.query.filter_by(book_id=book_id).first()
    review_info     = lib_reviews.query.filter_by(book_id=book_id).first()
    status_info     = lib_status.query.filter_by(book_id=book_id).first()

    if not status_info:
        flash("대여한 책이 없습니다.")
        return redirect(url_for('main.home'))
    else:
        db.session.add(status_info)
        db.session.commit()
        return redirect(url_for('info.html'))
        # return render_template('info.html', book_list=book_list, status_info=status_info, review_info=review_info)

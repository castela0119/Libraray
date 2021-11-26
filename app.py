from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    
    app.config.from_object(config) # config 에서 가져온 파일을 사용합니다.

    db.init_app(app)               # SQLAlchemy 객체를 app 객체와 이어줍니다.
    Migrate().init_app(app, db)
 
    
    from views import main_view, book_detail_view, status_view

    from models import models
    app.register_blueprint(main_view.bp)
    app.register_blueprint(book_detail_view.bp)
    app.register_blueprint(status_view.bp)

    app.secret_key = "seeeeeeeeeeeecret"
    app.config['SESSION_TYPE'] = 'filesystem'

    with app.app_context():
        # 만약 테이블이 없을 경우
        # models 에 정의된 테이블 구조를 만들어 준다
        # 있을 경우 작동 안함.
        db.create_all() 
        # TODO: 파이썬 패키지 검색

        # 테이블에 아무런 값이 없을떄( book 테이블) 실행 하면 값을 채워 준다.
        # from models.models import lib_books
        # from test import books as b

        # for item in b:
        #     book = lib_books()
        #     book.book_id = item[0]
        #     book.book_name = item[1]
        #     book.publisher = item[2]
        #     book.author = item[3]
        #     book.publication_date = item[4]
        #     book.pages = item[5]
        #     book.isbn = item[6]
        #     book.description = item[7]
        #     book.origin_url = item[8]
        #     book.img_path = f'book_img/{item[9]}'
        #     db.session.add(book)
        #     db.session.commit()

    
    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=3333)
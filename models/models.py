from app import db

'''
model.py
이 파일은 데이터베이스의 제약 조건을 명시하는 파일입니다.
관계형 데이터베이스의 데이터를 객체랑 연결 시켜주는 것을 ORM (Object Relational Mapping) 이라고 불러요.
즉, 이 파일은 외부에 존재하는 DB를 서버에서 사용하기 위해, DB와 동일한 제약조건을 객체에 걸어버리는 겁니다.
'''

class lib_books(db.Model):

    __tablename__ = 'lib_books'

    book_id             = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True,)
    book_name           = db.Column(db.String(30), nullable=False)
    publisher           = db.Column(db.String(50),)
    author              = db.Column(db.String(30),)
    publication_date    = db.Column(db.Integer,)
    pages               = db.Column(db.Integer,)
    isbn                = db.Column(db.Integer, nullable=False)
    description         = db.Column(db.String(255),)
    img_path            = db.Column(db.String(255),)

class lib_status(db.Model):

    __tablename__ = 'lib_status'

    status_no           = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True,)
    book_id             = db.Column(db.Integer, db.ForeignKey('lib_books.book_id'), nullable=False,)
    user_no             = db.Column(db.Integer, db.ForeignKey('lib_users.user_no'), nullable=False,)
    book_name           = db.Column(db.String(30), db.ForeignKey('lib_books.book_name'), nullable=False,)
    book_start          = db.Column(db.Integer,)
    book_end            = db.Column(db.Integer,)

class lib_users(db.Model):

    __tablename__ = 'lib_users'

    user_no             = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True,)
    user_email          = db.Column(db.String(40), nullable=False)
    user_pw             = db.Column(db.Integer, nullable=False)
    user_name           = db.Column(db.String(40), nullable=False)

from ..extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    hostel = db.Column(db.String(100), nullable=False)
    room_no = db.Column(db.String(20), nullable=False)
    role = db.Column(
        db.String(20),
        nullable=False,
        default="student"  
    )
    diaries = db.relationship('HostelDiary', backref='user', lazy=True)
    diary_comments = db.relationship('DiaryComment', backref='user', lazy=True)
    diary_likes = db.relationship('DiaryLike', backref='user', lazy=True)
    profile_pic = db.Column(db.String(255))




from app.extensions import db
from datetime import datetime

class Announcement(db.Model):
    __tablename__ = 'announcement'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    hostel = db.Column(db.String(50), nullable=True) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_pinned = db.Column(db.Boolean, default=False)



class Notification(db.Model):
    __tablename__ = "notification"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

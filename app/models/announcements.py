from app.extensions import db
from datetime import datetime

class Announcement(db.Model):
    __tablename__ = 'announcement'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    hostel = db.Column(db.String(50), nullable=True)  # None = all hostels
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

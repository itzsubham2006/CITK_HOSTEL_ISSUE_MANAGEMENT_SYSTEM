from app.extensions import db
from datetime import datetime

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(255), nullable=True)
    
  
    hostel = db.Column(db.String(100), nullable=False)  #  NEW

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    upvotes = db.Column(db.Integer, default=1)


    def __repr__(self):
        return f"<Complaint {self.id} - {self.category}>"


class ComplaintUpvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'complaint_id', name='unique_user_complaint_upvote'),
    )

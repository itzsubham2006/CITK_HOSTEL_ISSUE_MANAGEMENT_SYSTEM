from models import db

class complaints(db.Model):
    id = db.Column(db.Integer, primar_key = True)
    image_file = db.Column(db.String(30), nullable = False, default = 'default.jpg')
    
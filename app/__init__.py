from flask import Flask
from .config import Config
from .extensions import db, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    from .routes import auth_bp
    # from .routes.admin_routes import admin_bp
    # from .routes.students_routes import student_bp

    app.register_blueprint(auth_bp)
    # app.register_blueprint(admin_bp)
    # app.register_blueprint(student_bp)

    with app.app_context():
        db.create_all()

    return app


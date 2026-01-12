from flask import Flask
from .config import Config
from .extensions import db, bcrypt, login_manager
from flask_migrate import Migrate
from datetime import timedelta
from app import models
from app.models.announcements import Announcement
import os
from .routes import auth_bp
from .routes.students_routes import students_bp
from .routes.hostel_diary import diary_bp
from .routes.admin_routes import admin_bp
from app.routes.chatbot import chatbot_bp
    

login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"





migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)

   
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app) 
    migrate.init_app(app, db)
    

    UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


 
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(diary_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        
        
  
    @app.context_processor
    def inject_notification_count():
        count = Announcement.query.count()
        return dict(notification_count=count)


    return app


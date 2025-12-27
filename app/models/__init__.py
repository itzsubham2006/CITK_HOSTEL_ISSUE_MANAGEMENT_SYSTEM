from app.extensions import login_manager
from .user import User
from .complaints import Complaint
from .announcements import Announcement


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

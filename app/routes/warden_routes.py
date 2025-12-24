from flask import Blueprint, render_template, request
from flask_login import login_required
from ..models.complaints import Complaint
from ..utils.roles import role_required

warden_bp = Blueprint("warden", __name__, url_prefix="/warden")


@warden_bp.route("/dashboard")
@login_required
@role_required("warden")
def warden_dashboard():
    hostel = request.args.get("hostel")

    if hostel:
        complaints = Complaint.query.filter_by(hostel=hostel).all()
    else:
        complaints = Complaint.query.all()

    return render_template(
        "warden/dashboard.html",
        complaints=complaints,
        selected_hostel=hostel
    )

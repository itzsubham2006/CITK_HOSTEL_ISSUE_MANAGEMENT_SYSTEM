from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.extensions import db
from app.models.announcements import Announcement
from app.models.complaints import Complaint
from app.utils.roles import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    hostel = request.args.get("hostel")
    if hostel:
        complaints = Complaint.query.filter_by(hostel=hostel).all()
    else:
        complaints = Complaint.query.all()
    return render_template(
        "admin/dashboard.html",
        complaints=complaints,
        selected_hostel=hostel
    )


@admin_bp.route("/announcements", methods=["GET", "POST"])
@login_required
@admin_required
def announcements():
    if request.method == "POST":
        a = Announcement(
            title=request.form["title"],
            message=request.form["message"],
            hostel=request.form.get("hostel")
        )
        db.session.add(a)
        db.session.commit()
        flash("Announcement published", "success")
        return redirect(url_for("admin.announcements"))

    announcements = Announcement.query.order_by(
        Announcement.created_at.desc()
    ).all()
    return render_template("admin/announcements.html", announcements=announcements)



@admin_bp.route("/complaint/<int:id>/status", methods=["POST"])
@login_required
@admin_required
def update_status(id):
    complaint = Complaint.query.get_or_404(id)
    complaint.status = request.form["status"]
    db.session.commit()
    return redirect(request.referrer)

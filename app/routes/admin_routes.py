from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.extensions import db
from app.models.announcements import Announcement
from app.models.complaints import Complaint
from app.utils.roles import admin_required
from app.models.announcements import Notification
from flask_login import current_user

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



# ---------------------announcements------------------------------------
@admin_bp.route("/announcements", methods=["GET", "POST"])
@login_required
@admin_required
def announcements():
    if request.method == "POST":
        a = Announcement(
            title=request.form["title"],
            message=request.form["message"],
            hostel=request.form.get("hostel"),
            is_pinned=True if request.form.get("pin") else False
        )
        db.session.add(a)
        db.session.commit()

        
        n = Notification(
            message=f"{a.title} — {a.message[:80]}...",
            user_id=current_user.id  
        )
        db.session.add(n)
        db.session.commit()

        flash("Announcement published", "success")
        return redirect(url_for("admin.announcements"))

    announcements = Announcement.query.order_by(
        Announcement.is_pinned.desc(),
        Announcement.created_at.desc()
    ).all()

    return render_template("admin/announcements.html", announcements=announcements)





# ------------------------update_status--------------------
@admin_bp.route("/complaint/<int:id>/status", methods=["POST"])
@login_required
@admin_required
def update_status(id):
    complaint = Complaint.query.get_or_404(id)
    complaint.status = request.form["status"]
    db.session.commit()
    return redirect(request.referrer)





# -----------------edit_announcement------------------------
@admin_bp.route("/announcement/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_announcement(id):
    a = Announcement.query.get_or_404(id)

    if request.method == "POST":
        a.title = request.form["title"]
        a.message = request.form["message"]
        a.hostel = request.form.get("hostel")
        a.is_pinned = True if request.form.get("pin") else False
        db.session.commit()
        flash("Announcement updated", "success")
        return redirect(url_for("admin.announcements"))

    return render_template("admin/edit_announcement.html", a=a)




# ------------------delete_announcement------------------------
@admin_bp.route("/announcement/delete/<int:id>")
@admin_required
def delete_announcement(id):
    a = Announcement.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    flash("Announcement deleted", "danger")
    return redirect(url_for("admin.announcements"))




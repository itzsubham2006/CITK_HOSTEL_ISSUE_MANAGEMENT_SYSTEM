from flask import Blueprint, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from ..extensions import db
from ..models.complaints import Complaint
from ..forms import ComplaintForm
import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename


students_bp = Blueprint('students', __name__)





# -------------------------------------my complaints-------------------------------------
@students_bp.route('/my_complaints')
@login_required
def my_complaints():
    user_complaints = Complaint.query.filter_by(user_id=current_user.id).all()
    
    if not user_complaints:
        flash("Empty", "info")
        return redirect(url_for('students.report_issue')) 
    
    return render_template('student/my_issues.html', complaints=user_complaints)




# ----------------------------report issue--------------------------------
@students_bp.route("/report_issue", methods=['GET', 'POST'])
@login_required
def report_issue():
    form = ComplaintForm()

    if form.validate_on_submit():
        image_filename = None

       
        if form.image.data:
            image = form.image.data
            image_filename = f"{uuid.uuid4().hex}_{secure_filename(image.filename)}"

            upload_folder = os.path.join(
                current_app.root_path,
                "static/complaint_images"
            )

            
            os.makedirs(upload_folder, exist_ok=True)

          
            image.save(os.path.join(upload_folder, image_filename))

       
        new_issue = Complaint(
            category=form.category.data,
            description=form.description.data,
            image=image_filename,
            user_id=current_user.id,
            hostel=current_user.hostel 
        )

        db.session.add(new_issue)
        db.session.commit()

        flash('Your issue has been reported successfully!', 'success')
        return redirect(url_for('students.my_complaints'))

    return render_template('student/report_issue.html', form=form)



@students_bp.route("/dashboard")
@login_required
def dashboard():
    hostel = current_user.hostel

    complaints = Complaint.query.filter_by(hostel=hostel).all()

    return render_template(
        "student/dashboard.html",
        complaints=complaints,
        hostel=hostel
    )
    
    
    
@students_bp.route("/schedules")
@login_required
def schedules():
    return render_template("student/schedules.html")
    
    

    
@students_bp.route("/about")
@login_required
def about():
    return render_template("student/about.html")

    
@students_bp.route("/hostel_facility")
@login_required
def hostel_facility():
    return render_template("hostel/hostel_facility.html")
    
    
@students_bp.route("/all_issues")
@login_required
def all_issues():
    complaints = Complaint.query.filter_by(
        hostel=current_user.hostel
    ).order_by(Complaint.date_posted.desc()).all()

    return render_template(
        "student/all_issues.html",
        complaints=complaints,
        hostel=current_user.hostel
    )
    
    
    
    
@students_bp.route("/analytics")
@login_required
def analytics():
    hostel = current_user.hostel

    data = db.session.query(
        Complaint.status,
        func.count(Complaint.id)
    ).filter(
        Complaint.hostel == hostel
    ).group_by(Complaint.status).all()

    stats = {
        "Pending": 0,
        "In Progress": 0,
        "Resolved": 0
    }

    for status, count in data:
        stats[status] = count

    total = sum(stats.values())

    return render_template(
        "student/analytics.html",
        stats=stats,
        total=total,
        hostel=hostel
    )









@students_bp.route("/api/analytics")
@login_required
def analytics_api():
    hostel = current_user.hostel

    data = db.session.query(
        Complaint.status,
        func.count(Complaint.id)
    ).filter(
        Complaint.hostel == hostel
    ).group_by(Complaint.status).all()

    return jsonify({status: count for status, count in data})
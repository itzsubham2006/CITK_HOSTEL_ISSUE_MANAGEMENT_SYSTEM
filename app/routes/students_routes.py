from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
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
            hostel=current_user.hostel   #  auto
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
    
    
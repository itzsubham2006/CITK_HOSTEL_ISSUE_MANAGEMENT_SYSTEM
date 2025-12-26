from flask import Blueprint, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from ..extensions import db
from ..models.complaints import Complaint
from ..models.complaints import ComplaintUpvote
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


# ================================dashboard==============================
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
    
    
# =====================================schedules================================ 
@students_bp.route("/schedules")
@login_required
def schedules():
    return render_template("student/schedules.html")
    
    

# --------------------------------about----------------------------
@students_bp.route("/about")
@login_required
def about():
    return render_template("student/about.html")

# -----------------------------------------hostel_facility-------------------------------
@students_bp.route("/hostel_facility")
@login_required
def hostel_facility():
    return render_template("hostel/hostel_facility.html")



    
    
# ------------------------------issues-----------------------------------
@students_bp.route('/issues')
@login_required
def all_issues():
    complaints = Complaint.query \
        .filter_by(hostel=current_user.hostel) \
        .order_by(Complaint.upvotes.desc(), Complaint.date_posted.desc()) \
        .all()

    return render_template(
        'student/all_issues.html',
        complaints=complaints,
        hostel=current_user.hostel
    )
    
    

    
# -----------------------------------------analytics----------------------------------
@students_bp.route('/analytics')
@login_required
def analytics():
    hostel = current_user.hostel
    status_data = db.session.query(
        Complaint.status,
        func.count(Complaint.id)
    ).filter_by(hostel=hostel).group_by(Complaint.status).all()

    status_counts = {
        "Pending": 0,
        "In Progress": 0,
        "Resolved": 0
    }

    for status, count in status_data:
        status_counts[status] = count
   
    category_data = db.session.query(
        Complaint.category,
        func.count(Complaint.id)
    ).filter_by(hostel=hostel).group_by(Complaint.category).all()

    categories = [c[0] for c in category_data]
    category_counts = [c[1] for c in category_data]

    total_upvotes = db.session.query(
        func.count(ComplaintUpvote.id)
    ).join(Complaint).filter(
        Complaint.hostel == hostel
    ).scalar()

    total_issues = Complaint.query.filter_by(hostel=hostel).count()

    top_issues = Complaint.query.filter_by(
        hostel=hostel
    ).order_by(Complaint.upvotes.desc()).limit(5).all()
    
    top_issues_data = [
        {"category": issue.category, "upvotes": issue.upvotes}
        for issue in top_issues
    ]
    return render_template(
        "student/analytics.html",
        status_counts=status_counts,
        categories=categories,
        category_counts=category_counts,
        total_upvotes=total_upvotes,
        total_issues=total_issues,
        top_issues=top_issues_data  
    )




# ===========================upvote_complaint=====================================
@students_bp.route('/complaint/<int:cid>/upvote', methods=['POST'])
@login_required
def upvote_complaint(cid):

    complaint = Complaint.query.get_or_404(cid)

    
    existing = ComplaintUpvote.query.filter_by(
        user_id=current_user.id,
        complaint_id=cid
    ).first()

    if existing:
        return jsonify({'success': False, 'error': 'Already voted'})

    # add vote
    vote = ComplaintUpvote(
        user_id=current_user.id,
        complaint_id=cid
    )

    complaint.upvotes += 1

    db.session.add(vote)
    db.session.commit()

    return jsonify({
        'success': True,
        'upvotes': complaint.upvotes
    })

# ==============================importing all_stuffs=====================================================
from flask import Blueprint, jsonify, render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from sqlalchemy import func
from ..extensions import db
from ..models.user import User
from ..models.complaints import Complaint, ComplaintUpvote, HostelDiary
from ..forms import ComplaintForm
import os
import uuid
from app.models.announcements import Notification
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
    return render_template("publics/schedules.html")
    
    

# --------------------------------about----------------------------
@students_bp.route("/about")
@login_required
def about():
    return render_template("publics/about.html")

# -----------------------------------------hostel_facility-------------------------------
@students_bp.route("/hostel_facility")
@login_required
def hostel_facility():
    return render_template("hostel/hostel_facility.html")



    
    
# ------------------------------issues-----------------------------------
@students_bp.route("/issues")
@login_required
def all_issues():

    if current_user.role == 'admin':
        complaints = Complaint.query.order_by(Complaint.upvotes.desc()).all()
        hostel = "All Hostels"
    else:
        complaints = Complaint.query.filter_by(
            hostel=current_user.hostel
        ).order_by(Complaint.upvotes.desc()).all()
        hostel = current_user.hostel

    return render_template(
        "publics/all_issues.html",
        complaints=complaints,
        hostel=hostel
    )





# ------------------------------------notififcation------------------------------------
@students_bp.route("/notification")
@login_required
def notification():
    notifications = Notification.query.order_by(
        Notification.created_at.desc()
    ).all()

    return render_template(
        "publics/notification.html",
        notifications=notifications
    )
    
# -------------------delete_notification---------------------
@students_bp.route("/notifications/delete/<int:id>", methods=["POST"])
@login_required
def delete_notification(id):
    notification = Notification.query.get_or_404(id)
    db.session.delete(notification)
    db.session.commit()
    flash("Notification removed", "success")
    return redirect(url_for("students.notification"))


# -------------------------------clear_notifications-------------------
@students_bp.route("/clear_notifications", methods=["POST"])
@login_required
def clear_notifications():
    # Delete all notifications for the logged-in user
    try:
        Notification.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash("All notifications cleared successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error clearing notifications.", "danger")
        print(e)
    
    return redirect(url_for("students.notification"))




    
# -----------------------------------------analytics----------------------------------
@students_bp.route('/analytics')
@login_required
def analytics():

    is_admin = current_user.role == 'admin'

    # ---------- STATUS COUNTS ----------
    status_query = db.session.query(
        Complaint.status,
        func.count(Complaint.id)
    )

    if not is_admin:
        status_query = status_query.filter(
            Complaint.hostel == current_user.hostel
        )

    status_data = status_query.group_by(Complaint.status).all()

    status_counts = {
        "Pending": 0,
        "In Progress": 0,
        "Resolved": 0
    }

    for status, count in status_data:
        status_counts[status] = count


    # ---------- CATEGORY COUNTS ----------
    category_query = db.session.query(
        Complaint.category,
        func.count(Complaint.id)
    )

    if not is_admin:
        category_query = category_query.filter(
            Complaint.hostel == current_user.hostel
        )

    category_data = category_query.group_by(Complaint.category).all()

    categories = [c for c, _ in category_data]
    category_counts = [count for _, count in category_data]


    # ---------- TOTAL UPVOTES ----------
    upvote_query = db.session.query(
        func.count(ComplaintUpvote.id)
    ).join(Complaint)

    if not is_admin:
        upvote_query = upvote_query.filter(
            Complaint.hostel == current_user.hostel
        )

    total_upvotes = upvote_query.scalar() or 0


    # ------------------- TOTAL ISSUES -----------------
    issues_query = Complaint.query

    if not is_admin:
        issues_query = issues_query.filter(
            Complaint.hostel == current_user.hostel
        )

    total_issues = issues_query.count()


    # ---------------------- TOP ISSUES -----------------------
    top_query = Complaint.query.order_by(
        Complaint.upvotes.desc()
    )

    if not is_admin:
        top_query = top_query.filter(
            Complaint.hostel == current_user.hostel
        )

    top_issues = top_query.limit(5).all()

    top_issues_data = [
        {
            "category": issue.category,
            "upvotes": issue.upvotes
        }
        for issue in top_issues
    ]


    return render_template(
        "publics/analytics.html",
        status_counts=status_counts,
        categories=categories,
        category_counts=category_counts,
        total_upvotes=total_upvotes,
        total_issues=total_issues,
        top_issues=top_issues_data,
        hostel="All Hostels" if is_admin else current_user.hostel
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



# ================diary delete=============================
@students_bp.route('/delete-diary/<int:id>')
@login_required
def delete_diary(id):
    diary = HostelDiary.query.get_or_404(id)

    if diary.user_id != current_user.id:
        flash("You can't delete this photo", "danger")
        return redirect(url_for('students.profile'))

    image_path = os.path.join('app/static/uploads', diary.image)
    if os.path.exists(image_path):
        os.remove(image_path)

    db.session.delete(diary)
    db.session.commit()

    flash("Diary deleted successfully", "success")
    return redirect(url_for('students.profile'))




# ------------------delete_issues---------------------------
@students_bp.route('/delete-issues')
@login_required
def delete_issues():
    id = request.args.get('id', type=int)

    if not id:
        abort(404)

    issue = Complaint.query.get_or_404(id)

    if issue.user_id != current_user.id:
        flash("You are not allowed to delete this complaint.", "danger")
        return redirect(url_for('students.my_complaints'))

    # delete image if exists
    if issue.image:
        image_path = os.path.join(
            current_app.root_path,
            'static/complaint_images',
            issue.image
        )
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(issue)
    db.session.commit()

    flash("Complaint deleted successfully", "success")
    return redirect(url_for('students.my_complaints'))

    
    

# ==================================profile===============================
@students_bp.route('/profile')
@login_required
def profile():
    issues = Complaint.query.filter_by(user_id=current_user.id).all()
    diaries = HostelDiary.query.filter_by(user_id=current_user.id).all()
    return render_template('publics/profile.html', issues=issues, diaries=diaries)

# ==========================profile picture=================
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png','jpg','jpeg'}
           

# ---------------upload_profile_pic----------------------
@students_bp.route('/upload-profile-pic', methods=['POST'])
@login_required
def upload_profile_pic():
    file = request.files.get('profile_pic')

    if not file or file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('students.profile'))

    if not allowed_file(file.filename):
        flash('Invalid file type', 'danger')
        return redirect(url_for('students.profile'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

    file.save(filepath)

    current_user.profile_pic = filename
    db.session.commit()

    flash('Profile picture updated!', 'success')
    return redirect(url_for('students.profile'))



# -----------------cube----------------------------
@students_bp.route('/cube')
def cube():
    return render_template("cube/index.html")


# ------------------------organizational_structure-----------------------------
@students_bp.route('/organizational_structure')
def organizational_structure():
    return render_template("publics/organizational_structure.html")



# ---------------- HOSTEL ROOMS MAP ----------------
# routes.py
@students_bp.route("/hostel_rooms")
@login_required
def hostel_rooms():

    if current_user.role == "student":
        hostel = current_user.hostel
    else:
        hostel = request.args.get("hostel", current_user.hostel)

    users = User.query.filter_by(hostel=hostel).all()

    ROOM_CAPACITY = 2

    room_map = {}
    for u in users:
        room_map.setdefault(str(u.room_no), []).append({
            "name": u.username,
            "email": u.email,
            "id": u.id
        })

    is_staff = current_user.role in ["admin", "warden"]

    return render_template(
        "admin/hostel_rooms.html",
        hostel=hostel,
        room_map=room_map,
        is_staff=is_staff,
        capacity=ROOM_CAPACITY
    )



# ------------------anti_ragging-------------------------------------
@students_bp.route("/anti_ragging")
def anti_ragging():
    return render_template("publics/anti_ragging.html")

# ---------------submit_anti_ragging---------------------------------
@students_bp.route("/submit_anti_ragging", methods=["POST"])
def submit_anti_ragging():
    full_name = request.form.get("full_name")
    email = request.form.get("email")
    mobile = request.form.get("mobile")
    college = request.form.get("college")
    year = request.form.get("year")
    complaint = request.form.get("complaint")

    
    print("---- Anti Ragging Complaint ----")
    print(full_name, email, mobile, college, year, complaint)

   
    flash("Your complaint has been submitted successfully. Strict action will be taken.", "success")

    return redirect(url_for("anti_ragging"))




# ------------------help------------------------------
@students_bp.route('/help')
def help():
    return render_template('publics/help.html')


# ------------------internet------------------------------


@students_bp.route('/hostel_body')
def hostel_body():
    return render_template('hostel/hostel_body.html')


from app.models.user import Feedback
@students_bp.route('/feedback',methods=['GET', 'POST'])
def feedback():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        feedback = request.form.get("feedback")
        
        new_feedback = Feedback(username = username, email = email, feedback = feedback)
        
        db.session.add(new_feedback)
        db.session.commit()

        return render_template("publics/thankyou.html", name=username.title())

    return render_template("publics/feedback.html")
        
    
    

@students_bp.route('/thankyou')
def thankyou():
    return render_template("publics/thankyou.html")


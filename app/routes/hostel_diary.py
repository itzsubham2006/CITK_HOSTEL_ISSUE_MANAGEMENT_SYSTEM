from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from ..models.complaints import HostelDiary, DiaryLike, DiaryComment
from app.extensions import db
from werkzeug.utils import secure_filename
import os
import uuid

diary_bp = Blueprint('diary', __name__)

UPLOAD_FOLDER = 'app/static/uploads'

@diary_bp.route('/hostel_diaries', methods=['GET', 'POST'])
@login_required
def hostel_diaries():
    if request.method == 'POST':
        image = request.files['image']
        caption = request.form['caption']

        if image:
            ext = image.filename.rsplit('.', 1)[1]
            unique_filename = f"{uuid.uuid4().hex}.{ext}"

            image.save(os.path.join(UPLOAD_FOLDER, unique_filename))

            diary = HostelDiary(
                image=unique_filename,
                caption=caption,
                user_id=current_user.id
            )
            db.session.add(diary)
            db.session.commit()

        return redirect(url_for('diary.hostel_diaries'))

    diaries = HostelDiary.query.order_by(HostelDiary.date_posted.desc()).all()
    return render_template('publics/hostel_diaries.html', diaries=diaries)



@diary_bp.route('/like-diary/<int:id>', methods=['POST'])
@login_required
def like_diary(id):
    diary = HostelDiary.query.get_or_404(id)

    existing_like = DiaryLike.query.filter_by(
        user_id=current_user.id,
        diary_id=id
    ).first()

    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        return jsonify({'liked': False, 'count': len(diary.likes)})

    like = DiaryLike(user_id=current_user.id, diary_id=id)
    db.session.add(like)
    db.session.commit()

    return jsonify({'liked': True, 'count': len(diary.likes)})



@diary_bp.route('/comment-diary/<int:id>', methods=['POST'])
@login_required
def comment_diary(id):
    comment_text = request.form['comment']

    comment = DiaryComment(
        comment=comment_text,
        user_id=current_user.id,
        diary_id=id)
    
    db.session.add(comment)
    db.session.commit()
    
    return redirect(url_for('diary.hostel_diaries'))


@diary_bp.route('/delete-diary/<int:id>', methods=['POST'])
@login_required
def delete_diary(id):
    diary = HostelDiary.query.get_or_404(id)

    image_path = os.path.join(UPLOAD_FOLDER, diary.image)
    if os.path.exists(image_path):
        os.remove(image_path)

    db.session.delete(diary)
    db.session.commit()

    return redirect(url_for('diary.hostel_diaries'))

from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..forms import RegistrationForm, LoginForm
from ..extensions import db, bcrypt
from ..models.user import User
from flask_login import login_user, current_user, logout_user



auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            hostel=form.hostel.data,
            room_no=form.room_no.data
        )

        db.session.add(user)
        db.session.commit()


        flash("Account created successfully", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)





# ------------------ Login ------------------

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            
           
            next_page = request.args.get('next')
            flash("Welcome back!", "success")
            return redirect(next_page) if next_page else redirect(url_for('auth.home'))

        flash("Invalid username or password", "danger")

    return render_template("auth/login.html", title="login", form=form)




# ------------------ Home ------------------
@auth_bp.route("/home")
def home():
    return render_template("auth/home.html")



# --------------------logout_user---------------
@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.login"))

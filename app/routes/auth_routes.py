from flask import Blueprint, render_template, redirect, url_for, flash
from ..forms import RegistrationForm, LoginForm
from ..extensions import db, bcrypt
from ..models.user import User

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
    form = LoginForm()
    if form.validate_on_submit():
        flash("Welcome back!", "success")
        return redirect(url_for('auth.home'))

    return render_template("auth/login.html", title="login", form=form)




# ------------------ Home ------------------
@auth_bp.route("/home")
def home():
    return render_template("auth/home.html")

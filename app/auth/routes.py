from flask import Blueprint, redirect, render_template, flash, session, url_for
from app.models import User
from .forms import RegistrationForm, LoginForm, SetDisplayNameForm, ResetPasswordForm, ResetRequestForm
from app.extensions import bcrypt, db
from flask_login import login_required, login_user, logout_user, current_user
from .utils import send_email


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        gender = form.gender.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        user = User(username=username, email=email, password=hashed_password, gender=gender)
        
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}", "danger")
            return redirect(url_for("auth.register"))
        
        flash("Successfully created an account. Login in to access it", "success")
        return redirect(url_for("auth.set_display_name", username=username))

    return render_template("auth/register.html", form=form, title="Sign Up")


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have successfully logged in", "success")
            return redirect(url_for("main.home"))
        
        flash("Invalid email or password", "danger")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/login.html", form=form, title="Login")


@auth.route("/register/<username>/set_display_name", methods=["GET", "POST"])
def set_display_name(username):
    if current_user.is_authenticated:
        return redirect(url_for("profile.edit_profile"))
    
    form = SetDisplayNameForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()

        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
                
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}", "danger")
            return redirect(url_for("auth.login"))
        
        login_user(user)
        return redirect(url_for("main.home"))
    
    return render_template("auth/display_name.html", form=form, title="Login")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for("main.landing_page"))


@auth.route("/reset_request", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    form = ResetRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data)
        send_email(user)
        flash("An email containing the reset link was sent to you", "success")
        return redirect("auth.login")
    
    return render_template("auth/reset_request.html", form=form, title="Password Reset Request")
    

@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
     
    user = User.verify_reset_token(token)
    
    if not user:
        flash("Invalid or Expired token. Please try again")
        return redirect("auth/reset_request.html")

    form = ResetPasswordForm()  
    if form.validate_on_submit():

        if bcrypt.check_password_hash(user.password, form.password.data):
            flash("New password cannot be the same as old password", "danger")
            return redirect(url_for("auth.reset_password", token=token))
        
        new_password_hash = bcrypt.generate_password_hash(form.data)
        user.password = new_password_hash

        try:
            db.session.add(user)
            db.session.commit()
            flash("Successfully changed password. Login to access your account")
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}. Please try again", "danger")
        
        return redirect(url_for("auth.login"))
    
    return render_template("auth/reset_request.html", form=form, title="Password Reset Request")
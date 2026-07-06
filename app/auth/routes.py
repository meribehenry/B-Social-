from flask import Blueprint, redirect, render_template, flash, session, url_for
from app.services.token_service import TokenService
from .forms import RegistrationForm, LoginForm, ResetPasswordForm, ResetRequestForm, VerifyEmailForm
from app.extensions import db
from flask_login import login_required, logout_user, current_user
from app.services.auth_service import AuthService
import uuid
from app.models import User

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        auth_service = AuthService()
        user = auth_service.register_user(form)
        
        if user is not None:
            return redirect(url_for("auth.verify_email", user_public_id=user.public_id))  
        return redirect(url_for("auth.register"))

    return render_template("auth/register.html", form=form, title="Sign Up")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    form = LoginForm()

    if form.validate_on_submit():
        auth_service = AuthService()
        result = auth_service.sign_in(form)

        if result is True:
            return redirect(url_for("main.home"))
        else: 
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html", form=form, title="Login")


@auth.route("/verify_email/<user_public_id>", methods=["GET", "POST"])
def verify_email(user_public_id):
    form = VerifyEmailForm()

    if form.validate_on_submit():
        auth_service = AuthService()
        result = auth_service.verify_email(user_public_id, form.otp_code.data)

        if result is True:
            return redirect(url_for("main.home"))
        else:
            return redirect(url_for("auth.verify_email", user_public_id=user_public_id))

    user=User.query.filter_by(public_id=user_public_id).first()
    return render_template("auth/verify_email.html", form=form, title="Verify Email", user=user)


@auth.route("/resend_otp/<user_public_id>")
def resend_otp(user_public_id):
    auth_service = AuthService()
    auth_service.resend_otp(user_public_id)
    return redirect(url_for("auth.verify_email", user_public_id=user_public_id))


@auth.route("/logout")
@login_required
def logout():
    current_user.alternative_id = str(uuid.uuid4())
    db.session.commit()
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
        auth_service = AuthService()
        auth_service.reset_request(form)
        flash("If this account exist an email containing reset link was sent to it", "info") 
        return redirect(url_for("auth.login"))
    
    return render_template("auth/reset_request.html", form=form, title="Password Reset Request")
    

@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    token_service = TokenService()
    user = token_service.verify_reset_token(token)

    if not user:
        flash("Invalid or Expired token. Please try again", "danger")
        return redirect(url_for("auth.reset_request", token=token))

    form = ResetPasswordForm()  

    if form.validate_on_submit():
        auth_service = AuthService()
        result = auth_service.reset_password(form, user)
        if result is True:
            return redirect(url_for("auth.login"))
        else:
            return redirect(url_for("auth.reset_password", token=token))
    return render_template("auth/reset_password.html", form=form, title="Password Reset Request")
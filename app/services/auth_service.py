from app.extensions import bcrypt, db
from app.models import User, Profile
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_user
from app.services.email_service import EmailService
from app.services.otp_service import OTPService
from app.services.token_service import TokenService
from flask import flash
from flask_login import current_user
import uuid

class AuthService():
    
    def register_user(self, form):
        """ This function register users as unverified to the database"""
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            is_verified=False,
            gender=form.gender.data
        )

        profile = Profile(firstname=form.firstname.data, lastname=form.lastname.data, user=user)

        try:
            db.session.add(user)
            db.session.add(profile)
            db.session.commit()

        except SQLAlchemyError:
            db.session.rollback()
            flash(f"Error please try again", "danger")
            return None
        
        otp_service = OTPService()
        email_service = EmailService()

        otp = otp_service.generate_otp(form.email.data)
        email_service.send_otp(form.email.data, otp)
        return user
    

    def sign_in(self, form):
        """ This function logs user in"""
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):       
            login_user(user, remember=form.remember.data)
            flash("You have successfully logged in", "success")
            return True
        
        flash("Login failed. Please check your credentials and try again", "danger")
        return False
    
    
    def verify_email(self, user_public_id, otp_code):
        """ This function verifies user email and logs them in if they are unauthenticated"""

        user = User.query.filter_by(public_id=user_public_id).first()
        otp_service = OTPService()
        result = otp_service.verify_otp(otp_code, user.email)
        
        if result:
            user = User.query.filter_by(email=user.email).first()
            user.is_verified = True

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                flash(f"Error please try again", "danger")
                return None
            
            if not current_user.is_authenticated:
                login_user(user, remember=True)
                email_service = EmailService()
                # email_service.send_welcome_message() 

                
            flash("You can now explore B-Social", "success")
            return True
        
        flash("Invalid OTP code", "danger")
        return None


    def reset_request(self, form):
        token_service = TokenService()
        token = token_service.generate_reset_token(form.email.data)

        user = User.query.filter_by(email=form.email.data).first()
        if user:
            email_service = EmailService()
            email_service.send_request_token(token, email)    

    
    def reset_password(self, form, user):
        if bcrypt.check_password_hash(user.password, form.password.data):
            flash("New password cannot be the same as old password", "warning")
            return None
        
        user.password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.alternative_id = str(uuid.uuid4())

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash(f"Error please try again", "danger")
            return None
        
        flash("Successfully changed password. Login to access your account", "success")
        return True   

    def resend_otp(self, user_public_id): 
        user = User.query.filter_by(public_id=user_public_id).first()
        email_service = EmailService()
        otp = OTPService().generate_otp(user.email)
        email_service.send_otp(user.email, otp)
        flash("Email has been sent to you", "info")
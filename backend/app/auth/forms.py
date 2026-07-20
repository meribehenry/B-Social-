from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField, EmailField, PasswordField, RadioField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired, Length, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    firstname = StringField("Firstname:", validators=[DataRequired(), Length(min=3, max=20)])
    lastname = StringField("Lastname:", validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField("Username:", validators=[DataRequired(), Length(min=3, max=20)])
    email = EmailField("Email:", validators=[Email(), DataRequired(), Length(max=100)])
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=5, max=100)])
    confirm_password = PasswordField("Confirm Password:", validators=[EqualTo("password"), DataRequired()])
    gender = RadioField(choices=[("male", "Male"), ("female", "Female")], validators=[DataRequired()])
    submit = SubmitField("Sign Up")


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError(f"Username '{username.data}' already exists")
        
        if not username.data.isalnum():
            raise ValidationError(f"Username should only contain alphabets and number")
        

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError(f"Email '{email.data}' already exists")


class LoginForm(FlaskForm):
    email = EmailField("Email:", validators=[Email(), DataRequired(), Length(max=100)])
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=5, max=100)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class VerifyEmailForm(FlaskForm):
    otp_code = IntegerField("Otp Code", validators=[DataRequired()])
    submit = SubmitField("Verify")

class ResetRequestForm(FlaskForm):
    email = EmailField("Email:", validators=[Email(), DataRequired(), Length(max=100)])
    submit = SubmitField("Send Email")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data)

        if not user:
            raise ValidationError(f"Email '{email.data}' doesn't exists")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=5, max=100)])
    confirm_password = PasswordField("Confirm Password:", validators=[EqualTo("password"), DataRequired()])
    submit = SubmitField("Change Password")
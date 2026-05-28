from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length, ValidationError
from flask_wtf.file import FileAllowed, FileField
from app.models import User
from flask_login import current_user


class EditProfileForm(FlaskForm):
    firstname = StringField("Firstname:", validators=[Length(min=3, max=20)])
    lastname = StringField("Lastname:", validators=[Length(min=3, max=20)])
    username = StringField("Username:", validators=[Length(min=3, max=20)])
    bio = TextAreaField("Bio", validators=[Length(max=500)])
    profile_pic = FileField("Profile Picture", validators=[FileAllowed(["jpg", "img", "png", "png"])])
    submit = SubmitField("Save")


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if current_user.username != username.data:
            if user:
                raise ValidationError(f"Username '{username.data}' already exists")
            
            if not username.data.isalnum():
                raise ValidationError(f"Username should only contain alphabets and number")
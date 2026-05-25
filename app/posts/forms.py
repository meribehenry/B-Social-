from flask_wtf import FlaskForm
from wtforms import  SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import Length
from app.models import User


class NewPostForm(FlaskForm):
    content = TextAreaField("Content", validators=[Length(max=2000)])
    photo = FileField("Add Photo", validators=[FileAllowed(["jpg", "img", "jpeg", "png"])])
    submit = SubmitField("Post") 
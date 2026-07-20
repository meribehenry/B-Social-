from flask_wtf import FlaskForm
from wtforms import  SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    content = TextAreaField("Content", validators=[Length(max=500), DataRequired()])
    submit = SubmitField("Comment") 
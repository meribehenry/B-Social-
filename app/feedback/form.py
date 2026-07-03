from flask_wtf import FlaskForm
from wtforms import  SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class FeedbackForm(FlaskForm):
    text = TextAreaField("Content", validators=[Length(max=2000), DataRequired()])
    submit = SubmitField("Submit") 
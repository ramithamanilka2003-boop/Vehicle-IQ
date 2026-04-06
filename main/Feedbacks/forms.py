from flask_wtf import FlaskForm
from wtforms import RadioField,TextAreaField
from wtforms.validators import DataRequired,Length

class FeedbackForm(FlaskForm):
    rating = RadioField('Rating', coerce=int, choices=[
        (1, '★'), (2, '★ ★'), (3, '★ ★ ★'), (4, '★ ★ ★ ★'), (5, '★ ★ ★ ★ ★')
    ], validators=[DataRequired()])
    message = TextAreaField('Feedback', validators=[DataRequired(), Length(max=1000)])
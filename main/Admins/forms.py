from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DecimalField
from wtforms.validators import DataRequired,Email,NumberRange

class AdminLoginForm(FlaskForm):
    email=StringField("Email",
                      validators=[DataRequired(),Email()])
    
    password=PasswordField("Password",
                           validators=[DataRequired()])
    
    submit=SubmitField("Login")

class ConfigForm(FlaskForm):
    dollar_rate = DecimalField("Dollar Rate (LKR)", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Update Configuration")
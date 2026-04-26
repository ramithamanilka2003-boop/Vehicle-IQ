from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,SelectField
from wtforms.validators import DataRequired,Length


class BudgetRequestForm(FlaskForm):
    budget = SelectField(
        "Budget Range",
        choices=[
            ("5000000-6000000", "5,000,000 - 6,000,000"),
            ("6000000-7000000", "6,000,000 - 7,000,000"),
            ("7000000-8000000", "7,000,000 - 8,000,000"),
            ("8000000-9000000", "8,000,000 - 9,000,000"),
            ("9000000-10000000", "9,000,000 - 10,000,000"),
            ("10000000-11000000", "10,000,000 - 11,000,000"),
            ("11000000-12000000", "11,000,000 - 12,000,000"),
            ("12000000-15000000", "12,000,000 - 15,000,000"),

            # 15M to 60M with 10M gap
            ("15000000-25000000", "15,000,000 - 25,000,000"),
            ("25000000-35000000", "25,000,000 - 35,000,000"),
            ("35000000-65000000", "35,000,000 - 65,000,000"),
        ],
        validators=[DataRequired()]
    )


class AddBudgetForm(FlaskForm):
    model=StringField('Model',validators=[DataRequired(),Length(max=20)])
    year=IntegerField('Year',validators=[DataRequired()])
    price=IntegerField('Price',validators=[DataRequired()])
    submit = SubmitField('Submit')
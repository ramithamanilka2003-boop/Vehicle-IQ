from flask_wtf import FlaskForm
from wtforms import SubmitField,IntegerField,SelectField,BooleanField
from wtforms.validators import DataRequired,NumberRange

class VehiclePredictionForm(FlaskForm):
    model_year = IntegerField(
        "Model Year",
        validators=[DataRequired(), NumberRange(min=1990, max=2026)])
    
    milage = IntegerField(
        "Mileage (km)",
        validators=[DataRequired(), NumberRange(min=0)])

    transmission = SelectField(
    "Transmission",
    validators=[DataRequired()],  
    choices=[("1", "Auto"), ("0", "Manual")]
    )

    condition = SelectField(
    "Condition",
    validators=[DataRequired()],
    choices=[("1","Mint"), ("0","Medium")]
    )
    
    cc = IntegerField(
        "Engine CC",
        validators=[DataRequired(), NumberRange(min=600, max=5000)])

    age = IntegerField(
        "Vehicle Age",
        validators=[DataRequired(), NumberRange(min=0, max=50)])

    power_steering = BooleanField("Power Steering")
    push_start = BooleanField("Push Start")

    car_model = SelectField(
        "Car Model",
        validators=[DataRequired()],
        choices=[
            ("model_aqua", "Toyota Aqua"),
            ("model_aqua urban", "Toyota Aqua Urban"),
            ("model_corolla 121 g grade", "Corolla 121 G Grade"),
            ("model_corolla 121 lx grade", "Corolla 121 LX Grade"),
            ("model_corolla 121 x grade", "Corolla 121 X Grade"),
            ("model_toyota axio g grade", "Toyota Axio G Grade"),
            ("model_toyota axio wxb", "Toyota Axio WXB"),
            ("model_toyota premio", "Toyota Premio"),
            ("model_toyota premio g superior", "Premio G Superior"),
            ("model_vitz", "Toyota Vitz"),
            ("model_vitz safety", "Toyota Vitz Safety"),
            ("model_yaris", "Toyota Yaris"),
        ]
    )

    fuel_type = SelectField(
        "Fuel Type",
        validators=[DataRequired()],
        choices=[
            ("fuel_type_petrol", "Petrol"),
            ("fuel_type_diesel", "Diesel"),
            ("fuel_type_hybrid", "Hybrid"),
        ]
    )

    location = SelectField(
        "Location",
        validators=[DataRequired()],
        choices=[
            ("location_colombo", "Colombo"),
            ("location_galle", "Galle"),
            ("location_gampaha", "Gampaha"),
            ("location_homagama", "Homagama"),
            ("location_kadawatha", "Kadawatha"),
            ("location_kaluthara", "Kaluthara"),
            ("location_kandy", "Kandy"),
            ("location_kurunagala", "Kurunagala"),
            ("location_kurunegala", "Kurunegala"),
            ("location_maharagama", "Maharagama"),
            ("location_malabe", "Malabe"),
            ("location_matara", "Matara"),
            ("location_nugegoda", "Nugegoda"),
            ("location_others", "Others"),
            ("location_panadura", "Panadura"),
            ("location_piliyandala", "Piliyandala"),
            ("location_polonnaruwa", "Polonnaruwa"),
            ("location_rathnapura", "Rathnapura"),
        ]
    )

    vehicle_type = SelectField(
        "Vehicle Type",
        validators=[DataRequired()],
        choices=[
            ("car/sedan_car", "Hatchback"),
            ("car/sedan_sedan", "Sedan"),
        ]
    )

    color = SelectField(
        "Exterior Color",
        validators=[DataRequired()],
        choices=[
            ("ext_col_ash", "Ash"),
            ("ext_col_black", "Black"),
            ("ext_col_dark blue", "Dark Blue"),
            ("ext_col_desert sand mica", "Desert Sand Mica"),
            ("ext_col_grey", "Grey"),
            ("ext_col_lunar mist", "Lunar Mist"),
            ("ext_col_others", "Others"),
            ("ext_col_pearl white", "Pearl White"),
            ("ext_col_red", "Red"),
            ("ext_col_super white", "Super White"),
            ("ext_col_white", "White"),
            ("ext_col_wine red", "Wine Red"),
        ]
    )
    submit = SubmitField("Predict Price")
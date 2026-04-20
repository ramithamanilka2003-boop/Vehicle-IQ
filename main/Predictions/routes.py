from flask import render_template,url_for,redirect,flash,Blueprint
from main.Predictions.forms import VehiclePredictionForm
from main.models import Prediction
from flask_login import current_user,login_required
from main.Admins.decorator import admin_required
from main.Predictions.utils import convert_form_to_model_input,predict_price,apply_dollar_adjustment
from sqlalchemy.orm import joinedload
from main import db
from flask import current_app


prediction=Blueprint('prediction',__name__)

@prediction.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    form = VehiclePredictionForm()
    base_price = None
    adjusted_price =None

    if form.validate_on_submit():
        model = current_app.model
        model_columns = current_app.model_columns
        new_car = convert_form_to_model_input(form,model_columns)
        base_price = predict_price(new_car, model,model_columns)

        #dollar rate apply
        adjusted_price =base_price*apply_dollar_adjustment()

        prediction_record = Prediction(
            model=form.car_model.data,
            model_year=str(form.model_year.data),
            milage=form.milage.data,
            fuel_type=form.fuel_type.data,
            transmission=form.transmission.data,
            ext_col=form.color.data,
            type=form.vehicle_type.data,
            condition=form.condition.data,
            location=form.location.data,
            cc=form.cc.data,
            power_steering=form.power_steering.data,
            push_start=form.push_start.data,
            user_id=current_user.id,
            price=adjusted_price

        )
        db.session.add(prediction_record)
        db.session.commit()
        print("Prediction:", prediction)

    history = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.id.desc()).limit(5).all()

    return render_template("user/predict.html", form=form, prediction=adjusted_price , history=history)

@prediction.route('/admin/predictions')
@admin_required
def admin_predictions():
    if not current_user.is_admin:
        flash("Admin access only!", "danger")
        return redirect(url_for('admin.admin_login'))

    predictions = Prediction.query.options(joinedload(Prediction.user))\
                                  .order_by(Prediction.id.desc()).all()

    for p in predictions:
        print(p.id, p.user.username, p.model, p.price)

    return render_template(
        'admin/admin_predictions.html',
        predictions=predictions,
        active_nav='history' )


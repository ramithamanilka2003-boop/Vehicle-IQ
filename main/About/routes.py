from flask import render_template,url_for,redirect,flash,Blueprint,current_app
from main import db
from main.About.forms import AddvehicleForm
from main.models import Vehicles
from flask_login import current_user
from main.Admins.decorator import admin_required
from werkzeug.utils import secure_filename
import os


info=Blueprint('info',__name__)

@info.route("/about")
def about():
    vehicles = Vehicles.query.all()
    return render_template("user/about.html", vehicles=vehicles)

@info.route('/admin/vehicles')
@admin_required
def admin_vehicles():
    if not current_user.is_admin:
        flash("admin access only!", "danger")
        return redirect(url_for('admin.admin_login'))
    
    vehicles = Vehicles.query.order_by(Vehicles.id.desc()).all()
    
    return render_template("admin/admin_vehicle.html", vehicles=vehicles)

@info.route("/admin/add_vehicle", methods=["GET", "POST"])
@admin_required
def add_vehicle():
    form = AddvehicleForm()
    if form.validate_on_submit():

        photo_path = None

        if form.photo.data:
            photo_file = form.photo.data
            filename = secure_filename(photo_file.filename)

            upload_folder = os.path.join(current_app.root_path, "static/vehicles")
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            photo_file.save(os.path.join(upload_folder, filename))

            photo_path = f"vehicles/{filename}"

        new_vehicle = Vehicles(
            photo=photo_path,
            brand=form.brand.data,
            model=form.model.data,
            vehicle_category=form.vehicle_category.data,
            fuel_type=form.fuel_type.data
        )
        db.session.add(new_vehicle)
        db.session.commit()

        flash("Vehicle added successfully!", "success")
        return redirect(url_for("info.admin_vehicles"))

    return render_template("admin/admin_add_vehicle.html", form=form)



@info.route('/admin/vehicles/delete/<int:vehicle_id>', methods=['POST'])
@admin_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicles.query.get_or_404(vehicle_id)

    db.session.delete(vehicle)
    db.session.commit()

    flash("Vehicle deleted successfully!", "success")
    return redirect(url_for('info.admin_vehicles'))
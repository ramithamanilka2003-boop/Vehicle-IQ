from flask import render_template,url_for,redirect,flash,Blueprint
from main import app,bcrypt
from datetime import datetime
from main.Admins.forms import AdminLoginForm
from main.models import Admin, User, Prediction, Vehicles, Feedback
from flask_login import login_user,logout_user,login_required
from main.Admins.decorator import admin_required

admin=Blueprint('admin',__name__)

@admin.route("/admin/dashboard")
@login_required
@admin_required
def admin_dashboard():
    vehicles_count = Vehicles.query.count()
    predictions_count = Prediction.query.count()
    users_count = User.query.count()
    feedbacks_count = Feedback.query.count()
    
    # Fake a unified activity stream using the latest entries from different tables
    activities = []
    
    latest_vehicle = Vehicles.query.order_by(Vehicles.id.desc()).first()
    if latest_vehicle:
        time_str = latest_vehicle.created_at.strftime("%I:%M %p") if latest_vehicle.created_at else "Recent"
        activities.append({
            'icon': 'directions_car',
            'bg_class': 'bg-primary-fixed/20 text-primary-container',
            'title': 'Vehicle Added to Registry',
            'description': f"System appended {latest_vehicle.brand} {latest_vehicle.model} to the registry.",
            'time': time_str,
            'timestamp': latest_vehicle.created_at
        })
        
    latest_prediction = Prediction.query.order_by(Prediction.id.desc()).first()
    if latest_prediction:
        user = User.query.get(latest_prediction.user_id)
        username = user.username if user else "Unknown"
        time_str = latest_prediction.created_at.strftime("%I:%M %p") if latest_prediction.created_at else "Recent"
        activities.append({
            'icon': 'search',
            'bg_class': 'bg-tertiary-fixed/20 text-tertiary-container',
            'title': 'Prediction Executed',
            'description': f"User {username} performed a prediction for a {latest_prediction.model_year} {latest_prediction.model}.",
             'time': time_str,
             'timestamp': latest_prediction.created_at
        })
        
    latest_feedback = Feedback.query.order_by(Feedback.created_at.desc()).first()
    if latest_feedback:
        user = User.query.get(latest_feedback.user_id)
        username = user.username if user else "Unknown"
        time_str = latest_feedback.created_at.strftime("%I:%M %p") if latest_feedback.created_at else "Recent"
        activities.append({
            'icon': 'star',
            'bg_class': 'bg-secondary-fixed/30 text-on-secondary-container',
            'title': 'Feedback Received',
            'description': f'"{latest_feedback.message}" - {username}',
            'time': time_str,
            'timestamp': latest_feedback.created_at
        })

    # Sort activities by timestamp, newest first (treating None as oldest)
    activities.sort(key=lambda x: x['timestamp'] if x.get('timestamp') else datetime.min, reverse=True)
    
    return render_template("admin/admin_dashboard.html", 
        vehicles_count=vehicles_count,
        predictions_count=predictions_count,
        users_count=users_count,
        feedbacks_count=feedbacks_count,
        activities=activities
    )


@admin.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data.strip()):
            login_user(admin)
            return redirect(url_for("admin.admin_dashboard"))
        else:
            flash("Invalid email or password", "danger")
    return render_template("admin/admin_login.html", form=form)

@admin.route("/admin/logout")
@admin_required
def admin_logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("admin.admin_login"))
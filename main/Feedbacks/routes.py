from flask import render_template,url_for,redirect,flash,Blueprint
from main import db
from main.Feedbacks.forms import FeedbackForm
from main.models import Feedback
from flask_login import current_user,login_required
from main.Admins.decorator import admin_required
from sqlalchemy.orm import joinedload


feedbacks=Blueprint('feedbacks',__name__)

@feedbacks.route("/feedback",methods=["GET","POST"])
@login_required
def feedback():
    form=FeedbackForm()
    if form.validate_on_submit():
        feedback=Feedback(rating=form.rating.data,message=form.message.data,user_id=current_user.id)
        db.session.add(feedback)
        db.session.commit()
        flash("Thank you for your feedback","success")
        return redirect(url_for('index.home'))
    return render_template("user/feedback.html",form=form)

@feedbacks.route('/admin/feedback')
@admin_required
def admin_feedback():
    if not current_user.is_admin:
        flash("Admin access only!", "danger")
        return redirect(url_for('admin.admin_login'))

    feedbacks = Feedback.query.options(joinedload(Feedback.user))\
                              .order_by(Feedback.created_at.desc()).all()

    for f in feedbacks:
        print(f.id, f.user_id, f.user)

    return render_template(
        'admin/admin_feedback.html',
        feedbacks=feedbacks,
        active_nav='feedback'
    )

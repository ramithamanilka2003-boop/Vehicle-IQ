from flask import render_template,url_for,redirect,flash,Blueprint
from main import db
from main.Search.forms import BudgetRequestForm,AddBudgetForm
from main.models import Budgetrequest
from flask_login import current_user
from main.Admins.decorator import admin_required

searchs=Blueprint('searchs',__name__)

@searchs.route("/search", methods=["GET", "POST"])
def search():
    form = BudgetRequestForm()
    vehicles = None

    if form.validate_on_submit():
        budget_range = form.budget.data 

        min_price, max_price = map(int, budget_range.split("-"))

        vehicles = Budgetrequest.query.filter(
            Budgetrequest.price.between(min_price, max_price)
        ).all()

    return render_template("user/search.html", form=form, vehicles=vehicles)

@searchs.route('/admin/search')
@admin_required
def admin_search():
    if not current_user.is_admin:
        flash("admin access only!", "danger")
        return redirect(url_for('admin.admin_login'))
    
    budgetsearch = Budgetrequest.query.order_by(Budgetrequest.id.desc()).all()
    
    return render_template("admin/admin_budget_search.html", budgetsearch=budgetsearch)


@searchs.route('/admin/add', methods=["GET", "POST"])
@admin_required
def add_budget():
    form=AddBudgetForm()
    if form.validate_on_submit():
        budget=Budgetrequest(model=form.model.data,year=form.year.data,price=form.price.data)
        db.session.add(budget)
        db.session.commit()
        flash("Vehicle added successfully!", "success")
        return redirect(url_for("searchs.admin_search"))
    
    return render_template("admin/admin_add_budget.html", form=form)


@searchs.route('/admin/search/delete/<int:budget_id>', methods=['POST'])
@admin_required
def delete_budget_search(budget_id):
    budget = Budgetrequest.query.get_or_404(budget_id)

    db.session.delete(budget)
    db.session.commit()

    flash("Vehicle deleted successfully!", "success")
    return redirect(url_for('searchs.admin_search'))
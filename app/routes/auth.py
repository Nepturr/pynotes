from flask import Blueprint, render_template, redirect, url_for, flash, app
from flask_login import login_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm
import time

auth_bp = Blueprint("auth", __name__)



@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for(f"{user.role}.dashboard"))
        
        if not user:
            flash("L'email saisi est incorrect. Veuillez réessayer.", "danger")
            return render_template("login.html", form=form)

        if not user.check_password(form.password.data):
            flash("Le mot de passe est incorrect. Veuillez réessayer.", "danger")
        time.sleep(3)
    return render_template("login.html", form=form)




@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie.", "info")
    return redirect(url_for("auth.login"))




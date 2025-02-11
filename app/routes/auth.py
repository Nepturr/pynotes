import requests
from flask import Blueprint, render_template, redirect, url_for, flash, request, app
from flask_login import login_user, logout_user, login_required
from app.models import User, db
from app.forms import LoginForm, RegistrationForm
import time

auth_bp = Blueprint("auth", __name__)


def verify_recaptcha(response):
    """Vérifie la réponse reCAPTCHA en appelant l'API Google."""
    secret_key = app.config["RECAPTCHA_PRIVATE_KEY"]
    data = {"secret": secret_key, "response": response}
    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
    result = r.json()
    return result.get("success", False)


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




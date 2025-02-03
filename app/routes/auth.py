from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models import User, db
from app.forms import LoginForm, RegistrationForm

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Connexion réussie.", "success")
            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))
            elif user.role == "student":
                return redirect(url_for("student.dashboard"))
            elif user.role == "teacher":
                return redirect(url_for("teacher.dashboard"))
            else: 
                return redirect(url_for("main.index"))
        flash("Identifiants incorrects.", "danger")
    return render_template("login.html", form=form)



@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie.", "info")
    return redirect(url_for("auth.login"))



@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Ce nom d'utilisateur est déjà pris.", "danger")
        else:
            user = User(username=form.username.data, password=form.password.data, role="user")
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Compte créé avec succès. Vous pouvez vous connecter.", "success")
            return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

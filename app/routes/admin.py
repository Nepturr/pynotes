from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, db
from app.forms import RegistrationForm

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("main.index"))
    users = User.query.all()
    return render_template("admin/dashboard.html", users=users)

@admin_bp.route("/add_user", methods=["GET", "POST"])
@login_required
def add_user():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("main.index"))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Cet email est déjà utilisé.", "danger")
            return redirect(url_for("admin.add_user"))

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        new_user.set_password(form.password.data)

        try:
            db.session.add(new_user)
            db.session.commit()

            flash("Utilisateur créé avec succès.", "success")
            return redirect(url_for("admin.dashboard"))
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de l'ajout de l'utilisateur : {e}")  # Affichage de l'erreur en console
            flash("Une erreur est survenue lors de l'ajout.", "danger")

    return render_template("admin/add_user.html", form=form)

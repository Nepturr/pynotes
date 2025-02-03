# teacher.py

from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Grade, Class, db, Student
from app.forms import ClassForm

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")

@teacher_bp.route("/dashboard")
@login_required
def dashboard():
    users = User.query.all()
    return render_template("teacher/dashboard.html", users=users)

@teacher_bp.route("/manage_notes")
@login_required
def manage_notes():
    if current_user.role != "teacher":
        return jsonify({"error": "Accès non autorisé"}), 403

    students = Student.query.all() 

    return render_template("teacher/managenotes.html", students=students)

@teacher_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]

        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email

        if password:
            current_user.set_password(password)

        db.session.commit()
        flash("Profil mis à jour avec succès !", "success")
        return redirect(url_for("teacher.profile"))

    return render_template("teacher/profile.html")

@teacher_bp.route("/manage_classes")
@login_required
def manage_classes():
    classes = Class.query.all()
    form = ClassForm()  
    return render_template("teacher/manageclass.html", classes=classes, form=form)

@teacher_bp.route("/add_class", methods=["POST"])
@login_required
def add_class():
    form = ClassForm()
    if form.validate_on_submit():
        new_class = Class(name=form.name.data)
        db.session.add(new_class)
        db.session.commit()
        return jsonify({"success": True, "name": new_class.name, "id": new_class.id})
    
    return jsonify({"success": False, "errors": form.errors})



from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, Grade, db


student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.route("/dashboard")
@login_required
def dashboard():
    users = User.query.all()
    return render_template("student/dashboard.html", users=users)


@student_bp.route("/grades")
@login_required
def grades():
    student = current_user.student
    
    if student:
        grades = Grade.query.filter_by(student_id=student.id).join(Grade.subject).join(Grade.teacher).all()
        return render_template("student/grades.html", grades=grades)
    else:
        flash("Aucune donnée trouvée pour l'étudiant", "error")
        return redirect(url_for("student.dashboard"))


@student_bp.route("/profile", methods=["GET", "POST"])
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
        return redirect(url_for("student.profile"))
    
    return render_template("student/profile.html")
# teacher.py
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Grade, Class, db, Student, Subject, Teacher
from app.forms import ClassForm, GradeForm

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

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        flash("Vous n'êtes pas assigné comme professeur.", "danger")
        return redirect(url_for("teacher.dashboard"))

    classes = Class.query.all()
    return render_template("teacher/managenotes.html", classes=classes, teacher=teacher)

@teacher_bp.route("/teacher/add_notes", methods=["POST"])
@login_required
def add_notes():
    if current_user.role != "teacher":
        return jsonify({"error": "Accès non autorisé"}), 403
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Requête invalide, aucun JSON reçu"}), 400

        student_id = data.get("student_id")
        grade_value = data.get("grade")
        subject_id = data.get("subject_id")

        if not student_id or not grade_value or not subject_id:
            return jsonify({"error": "Données manquantes"}), 400

        teacher = Teacher.query.filter_by(user_id=current_user.id).first()
        if not teacher or not teacher.subject:
            return jsonify({"error": "Aucune matière associée"}), 404
    
        student = Student.query.get(student_id)
        if not student:

            return jsonify({"error": "Élève non trouvé"}), 404

        new_grade = Grade(
            student_id=student_id, subject_id=subject_id, teacher_id=teacher.id,
            grade=grade_value, date_added=datetime.utcnow()
        )
        db.session.add(new_grade)
        db.session.commit()
        
        return jsonify({"success": True, "grade": float(new_grade.grade), "student_id": student_id})

    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500


@teacher_bp.route("/delete_grade", methods=["POST"])
@login_required
def delete_grade():
    if current_user.role != "teacher":
        return jsonify({"error": "Accès non autorisé"}), 403
    
    data = request.get_json()
    grade_id = data.get("grade_id")
    
    grade = Grade.query.get_or_404(grade_id)
    db.session.delete(grade)
    db.session.commit()
    
    return jsonify({"success": True})




@teacher_bp.route('/get_student_grades/<int:student_id>', methods=['GET'])
@login_required
def get_student_grades(student_id):
    if current_user.role != "teacher":
        return jsonify({"error": "Accès non autorisé"}), 403

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({"error": "Professeur non trouvé"}), 404

    grades = Grade.query.filter_by(student_id=student_id, teacher_id=teacher.id).all()

    grade_data = [{
        "id": grade.id,
        "grade": float(grade.grade)
    } for grade in grades]

    return jsonify({"grades": grade_data})





@teacher_bp.route("/get_students/<int:class_id>")
@login_required
def get_students(class_id):
    if current_user.role != "teacher":
        return jsonify({"error": "Accès non autorisé"}), 403

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({"error": "Professeur non trouvé"}), 404

    subject = teacher.subject 
    if not subject:
        return jsonify({"error": "Aucune matière associée"}), 404

    students = Student.query.filter_by(class_id=class_id).all()
    student_data = []

    for student in students:
        grades = Grade.query.filter_by(student_id=student.id, subject_id=subject.id).all()
        student_data.append({
            "id": student.id,
            "name": f"{student.user.first_name} {student.user.last_name}",
            "grades": [{
                "id": grade.id,
                "grade": float(grade.grade)
            } for grade in grades]
        })

    return jsonify(student_data)

    

@teacher_bp.route('/get_subjects', methods=['GET'])
@login_required
def get_subjects():
    # Assurez-vous que le professeur a bien une matière assignée
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if teacher and teacher.subject:
        return jsonify([{"id": teacher.subject.id, "name": teacher.subject.name}])
    else:
        return jsonify({"success": False, "message": "Aucune matière associée à ce professeur"}), 404




@teacher_bp.route("/update_grade/<int:grade_id>", methods=["POST"])
@login_required
def update_grade(grade_id):
    if current_user.role != "teacher":
        return jsonify({"error": "Accès non autorisé"}), 403

    form = GradeForm()
    if form.validate_on_submit():
        grade = Grade.query.get_or_404(grade_id)
        grade.subject_id = form.subject.data
        grade.grade = form.grade.data
        db.session.commit()
        return jsonify({"success": True, "grade": float(grade.grade), "subject": grade.subject.name})
    
    return jsonify({"success": False, "errors": form.errors}), 400



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



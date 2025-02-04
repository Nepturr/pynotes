from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import User, Class, Subject, db, Teacher, Student
from werkzeug.security import generate_password_hash
from app.forms import AddClassForm, AddSubjectForm, AddUserForm

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("main.index"))

    form = AddUserForm()

    if form.validate_on_submit():
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data, method='pbkdf2:sha256'),
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Utilisateur ajouté avec succès.", "success")
        return redirect(url_for("admin.dashboard"))

    users = User.query.all()
    classes = Class.query.all()  # 🔹 Ajout des classes
    subjects = Subject.query.all()  # 🔹 Ajout des matières

    return render_template("admin/dashboard.html", form=form, users=users, classes=classes, subjects=subjects)


@admin_bp.route('/admin/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    class_id = data.get('class')  # Récupération de la classe sélectionnée
    subject_id = data.get('subject')

    if not (first_name and last_name and email and password and role):
        return jsonify({'success': False, 'error': 'Tous les champs sont obligatoires.'}), 400

    hashed_password = generate_password_hash(password)

    # Création de l'utilisateur
    new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.flush()  # Permet d'obtenir l'ID avant commit

    if role == "student":
        new_student = Student(user_id=new_user.id, class_id=class_id)
        db.session.add(new_student)

    elif role == "teacher":
        new_teacher = Teacher(user_id=new_user.id, subject_id=subject_id)
        db.session.add(new_teacher)

    db.session.commit()

    return jsonify({
        'success': True,
        'id': new_user.id,
        'first_name': new_user.first_name,
        'last_name': new_user.last_name,
        'email': new_user.email,
        'role': new_user.role
    })

@admin_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'error': 'Utilisateur non trouvé'}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route("/createclass", methods=["GET", "POST"])
@login_required
def createclass():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("main.index"))
    
    form = AddClassForm()  

    if form.validate_on_submit():
        new_class = Class(name=form.name.data)
        db.session.add(new_class)
        db.session.commit()
        flash("Classe ajoutée avec succès.", "success")
        return redirect(url_for("admin.createclass"))

    classes = Class.query.all()
    return render_template("admin/createclass.html", form=form, classes=classes)

# ADD CLASS AJAX
@admin_bp.route("/add_class", methods=["POST"])
@login_required
def add_class():
    if current_user.role != "admin":
        return jsonify({"success": False, "error": "Accès refusé."}), 403
    
    data = request.get_json()
    class_name = data.get("name")
    
    if not class_name:
        return jsonify({"success": False, "error": "Le nom de la classe est requis."}), 400
    
    existing_class = Class.query.filter_by(name=class_name).first()
    if existing_class:
        return jsonify({"success": False, "error": "Une classe avec ce nom existe déjà."}), 400
    
    new_class = Class(name=class_name)
    db.session.add(new_class)
    db.session.commit()
    
    return jsonify({"success": True, "id": new_class.id, "name": new_class.name})


@admin_bp.route("/delete_class/<int:class_id>", methods=["DELETE"])
@login_required
def delete_class(class_id):
    if current_user.role != "admin":
        return jsonify({"success": False, "error": "Accès refusé."}), 403

    class_to_delete = Class.query.get(class_id)
    if not class_to_delete:
        return jsonify({"success": False, "error": "Classe introuvable."}), 404

    db.session.delete(class_to_delete)
    db.session.commit()

    return jsonify({"success": True})

@admin_bp.route("/subjects", methods=["GET", "POST"])
@login_required
def subjects():
    if current_user.role != "admin":
        flash("Accès refusé.", "danger")
        return redirect(url_for("main.index"))
    
    form = AddSubjectForm() 

    if form.validate_on_submit():  
        new_subject = Subject(name=form.name.data)
        db.session.add(new_subject)
        db.session.commit()
        flash("Matière ajoutée avec succès.", "success")
        return redirect(url_for("admin.subjects"))

    subjects = Subject.query.all()
    return render_template("admin/subjects.html", form=form, subjects=subjects)

@admin_bp.route("/add_subject", methods=["POST"])
@login_required
def add_subject():
    if current_user.role != "admin":
        return jsonify({"success": False, "error": "Accès refusé."}), 403
    
    data = request.get_json()
    subject_name = data.get("name")
    
    if not subject_name:
        return jsonify({"success": False, "error": "Le nom de la matière est requis."}), 400
    
    existing_subject = Subject.query.filter_by(name=subject_name).first()
    if existing_subject:
        return jsonify({"success": False, "error": "Une matière avec ce nom existe déjà."}), 400
    
    new_subject = Subject(name=subject_name)
    db.session.add(new_subject)
    db.session.commit()
    
    return jsonify({"success": True, "id": new_subject.id, "name": new_subject.name})

@admin_bp.route("/delete_subject/<int:subject_id>", methods=["DELETE"])
@login_required
def delete_subject(subject_id):
    if current_user.role != "admin":
        return jsonify({"success": False, "error": "Accès refusé."}), 403

    subject_to_delete = Subject.query.get(subject_id)
    if not subject_to_delete:
        return jsonify({"success": False, "error": "Matière introuvable."}), 404

    db.session.delete(subject_to_delete)
    db.session.commit()

    return jsonify({"success": True})
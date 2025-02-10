from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db 

def create_admin():
    with db.session.begin(): 
        admin_exists = User.query.filter_by(role="admin").first()

        if not admin_exists:
            admin = User(
                first_name="admin",
                last_name="admin",
                email="admin@example.com",
                password=generate_password_hash("admin", method='pbkdf2:sha256'),
                role="admin"
            )
            db.session.add(admin)
            print("[INFO] Compte administrateur créé avec succès !")
        else:
            print("[INFO] Un administrateur existe déjà.")



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Enum('admin', 'teacher', 'student'), nullable=False)

    student = db.relationship('Student', back_populates='user', uselist=False)
    teacher = db.relationship('Teacher', back_populates='user', uselist=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} - Role {self.role}>"


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), unique=True, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='SET NULL'), nullable=True)

    user = db.relationship('User', back_populates='student', lazy="joined")
    class_ref = db.relationship('Class', back_populates='students', lazy="joined")
    grades = db.relationship('Grade', back_populates='student', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student {self.user.first_name} {self.user.last_name} - Class {self.class_ref.name if self.class_ref else 'N/A'}>"


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), unique=True, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='SET NULL'), nullable=True)

    user = db.relationship('User', back_populates='teacher', lazy="joined")
    subject = db.relationship('Subject', back_populates='teacher', lazy="joined")

    def __repr__(self):
        return f"<Teacher {self.user.first_name} {self.user.last_name}>"


class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    students = db.relationship('Student', back_populates='class_ref', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Class {self.name}>"


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    teacher = db.relationship('Teacher', back_populates='subject', lazy="joined")
    grades = db.relationship('Grade', back_populates='subject', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Subject {self.name}>"


class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    grade = db.Column(db.Numeric(5, 2), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('Student', back_populates='grades', lazy="joined")
    subject = db.relationship('Subject', back_populates='grades', lazy="joined")
    teacher = db.relationship('Teacher', lazy="joined")

    def __repr__(self):
        return f"<Grade {self.subject.name} - {self.grade}>"

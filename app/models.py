from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db 



def create_admin():

    with db.session.begin(): 
        if not User.query.filter_by(username="admin").first():
            admin = User(
                username="admin",
                email="admin@example.com",
                password=generate_password_hash("admin", method='pbkdf2:sha256'),
                role="admin"
            )
            db.session.add(admin)
            print("[INFO] Compte administrateur créé avec succès !")
        else:
            print("[INFO] Compte administrateur déjà existant.")



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")

    student = db.relationship('Student', back_populates='user', uselist=False)
    teacher = db.relationship('Teacher', back_populates='user', uselist=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.username} - Role {self.role}>"
    
    


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='SET NULL'), nullable=True)

    user = db.relationship('User', back_populates='student', lazy="joined")
    class_ref = db.relationship('Class', back_populates='students', lazy="joined")
    notes = db.relationship('Note', back_populates='student', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student {self.user.username} - Class {self.class_ref.name if self.class_ref else 'N/A'}>"


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    user = db.relationship('User', back_populates='teacher', lazy="joined")
    subjects = db.relationship('Subject', back_populates='teacher', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Teacher {self.user.username}>"


class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    students = db.relationship('Student', back_populates='class_ref', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Class {self.name}>"


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='SET NULL'))

    teacher = db.relationship('Teacher', back_populates='subjects', lazy="joined")
    notes = db.relationship('Note', back_populates='subject', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Subject {self.name} - Teacher {self.teacher.user.username if self.teacher else 'N/A'}>"


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    grade = db.Column(db.Numeric(5, 2), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('Student', back_populates='notes', lazy="joined")
    subject = db.relationship('Subject', back_populates='notes', lazy="joined")

    def __repr__(self):
        return f"<Note {self.subject.name} - {self.grade}>"


class Timetable(db.Model):
    __tablename__ = 'timetables'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete="CASCADE"), nullable=False)
    day = db.Column(db.String(15), nullable=False) 
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete="CASCADE"), nullable=False)

    class_ref = db.relationship('Class', lazy="joined")
    subject = db.relationship('Subject', lazy="joined")

    def __repr__(self):
        return f"<Timetable {self.class_ref.name if self.class_ref else 'N/A'} - {self.day} - {self.subject.name}>"



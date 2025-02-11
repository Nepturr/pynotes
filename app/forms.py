from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, SelectField
from flask_wtf.recaptcha import RecaptchaField
from wtforms.validators import DataRequired, Length
from app.models import Class, db


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    recaptcha = RecaptchaField() 
    submit = SubmitField("Se connecter")




class ProfileForm(FlaskForm):
    first_name = StringField('Prénom', validators=[DataRequired()])
    last_name = StringField('Nom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Mot de passe')

class ClassForm(FlaskForm):
    name = StringField("Nom de la classe", validators=[DataRequired()])
    submit = SubmitField("Ajouter la classe")


class AddClassForm(FlaskForm):
    name = StringField('Nom de la classe', validators=[DataRequired()])


class AddSubjectForm(FlaskForm):
    name = StringField('Nom de la matière', validators=[DataRequired(), Length(min=1, max=100)])


class AddUserForm(FlaskForm):
    first_name = StringField('Prénom', validators=[DataRequired(), Length(min=1, max=100)])
    last_name = StringField('Nom', validators=[DataRequired(), Length(min=1, max=100)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Rôle', choices=[('admin', 'Administrateur'), ('teacher', 'Enseignant'), ('student', 'Étudiant')], validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)


class GradeForm(FlaskForm):
    subject = SelectField("Matière", coerce=int, validators=[DataRequired()])
    grade = DecimalField("Note", places=2, validators=[DataRequired()])
    submit = SubmitField("Enregistrer")
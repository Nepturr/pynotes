from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app.models import User, Class, db


class LoginForm(FlaskForm):
    email = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")


from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=6)])
    role = SelectField("Rôle", choices=[("student", "Élève"), ("teacher", "Professeur"),  ("admin", "Admin")], validators=[DataRequired()])
    
    class_choice = SelectField("Affecter une classe", choices=[], coerce=int) 
    new_class = StringField("Créer une nouvelle classe") 
    submitClass = SubmitField("Créer la Classe")
    submit = SubmitField("Créer l'utilisateur")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_choice.choices = [(0, "Aucune")] + [(c.id, c.name) for c in Class.query.all()]



from flask_wtf import FlaskForm

class ClassForm(FlaskForm):
    name = StringField("Nom de la classe", validators=[DataRequired()])
    submit = SubmitField("Ajouter la classe")


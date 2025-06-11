from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, PasswordField  # Updated TextField → StringField
from wtforms.validators import DataRequired  # Updated Required → DataRequired



class RegisterForm(FlaskForm):
    user = StringField(u'Utilisateur', validators=[DataRequired()])  # Fixed
    password = PasswordField(u'Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField(u'Confirmer le mot de passe', validators=[DataRequired()])
    name = StringField(u'Nom')
    email = StringField(u'Adresse email', validators=[DataRequired()])
    telephone = StringField(u'Numéro de téléphone')

class LoginForm(FlaskForm):
    user = StringField(u'Utilisateur', validators=[DataRequired()])  # Fixed
    password = PasswordField(u'Mot de passe', validators=[DataRequired()])

class ExampleForm(FlaskForm):
    title = StringField(u'Titre', validators=[DataRequired()])  # Fixed
    content = TextAreaField(u'Contenu')
    date = DateTimeField(u'Date', format='%d/%m/%Y %H:%M')

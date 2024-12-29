from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FloatField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class SignupForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[
        DataRequired(), Length(min=4, max=100)
    ])
    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(max=150)
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(), Length(min=8, max=200)
    ])
    confirm_password = PasswordField('Confirmez le mot de passe', validators=[
        DataRequired(), EqualTo('password', message='Les mots de passe doivent correspondre.')
    ])
    first_name = StringField('Prénom', validators=[
        DataRequired(), Length(max=50)
    ])
    last_name = StringField('Nom', validators=[
        DataRequired(), Length(max=50)
    ])
    status = SelectField('Statut', choices=[
        ('proprietaire', 'Propriétaire'), ('locataire', 'Locataire')
    ], validators=[DataRequired()])
    submit = SubmitField('S\'enregistrer')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email()
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired()
    ])
    submit = SubmitField('Se connecter')



class RoomForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Prix', validators=[DataRequired()])
    location = StringField('Emplacement', validators=[DataRequired()])
    distance = FloatField('Distance (km)', validators=[DataRequired()])
    images = StringField('Images (séparées par des virgules)', validators=[Optional()])
    submit = SubmitField('Ajouter la chambre')

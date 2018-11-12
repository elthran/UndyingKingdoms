from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    username = StringField('Username', [DataRequired(message='You must enter a username.')])
    email = StringField('Email Address', validators=[Email(), DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password',
                             [DataRequired(message='You must enter a password.'),
                              Length(min=4),
                              EqualTo('confirmation', message='Passwords must match.')])
    confirmation = PasswordField('Repeat password')



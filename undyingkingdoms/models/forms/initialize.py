from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from wtforms.validators import DataRequired, Email, Length, EqualTo


class InitializeForm(FlaskForm):
    county = StringField('County', [DataRequired(message='You must enter a name for your county.')])
    leader = StringField('Leader', [DataRequired(message='You must enter a name for your leader.')])
    gender = StringField('Gender', [DataRequired(message='You must choose a gender.')])
    race = StringField('Race', [DataRequired(message='You must choose a race.')])



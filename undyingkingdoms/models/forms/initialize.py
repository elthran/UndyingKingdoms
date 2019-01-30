from flask_wtf import FlaskForm
from wtforms import StringField, SelectField

from wtforms.validators import DataRequired, NoneOf


class InitializeForm(FlaskForm):
    county = StringField('County', [DataRequired(message='You must enter a name for your county.')])
    leader = StringField('Leader', [DataRequired(message='You must enter a name for your leader.')])
    gender = SelectField('Gender', coerce=int, validators=[NoneOf([0], message='Must choose gender.')])
    race = SelectField('Race', coerce=int, validators=[NoneOf([0], message='Must choose race.')])
    title = SelectField('Title', coerce=int, validators=[NoneOf([0], message='Must choose title.')])



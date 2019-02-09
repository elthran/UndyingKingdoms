from flask_wtf import FlaskForm
from wtforms import StringField, SelectField

from wtforms.validators import DataRequired, NoneOf, Length


class InitializeForm(FlaskForm):
    county = StringField('County', validators=[DataRequired(message='You must enter a name for your county.'),
                                               Length(min=2, max=20)])
    leader = StringField('Leader', validators=[DataRequired(message='You must enter a name for your leader.'),
                                               Length(min=2, max=20)])
    title = SelectField('Title', coerce=int, validators=[NoneOf([0], message='Must choose title.')])
    race = SelectField('Race', coerce=int, validators=[NoneOf([0], message='Must choose race.')])
    background = SelectField('Background', coerce=int, validators=[NoneOf([0], message='Must choose background.')])



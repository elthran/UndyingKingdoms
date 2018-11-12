from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import NumberRange


class MilitaryForm(FlaskForm):
    peasant = IntegerField('peasant', validators=[NumberRange(min=0, max=None)], default=0)
    archer = IntegerField('archer', validators=[NumberRange(min=0, max=None)], default=0)
    soldier = IntegerField('soldier', validators=[NumberRange(min=0, max=None)], default=0)
    elite = IntegerField('elite', validators=[NumberRange(min=0, max=None)], default=0)



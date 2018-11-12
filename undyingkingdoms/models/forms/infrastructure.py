from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import NumberRange


class InfrastructureForm(FlaskForm):
    houses = IntegerField('houses', validators=[NumberRange(min=0, max=None)], default=0)
    fields = IntegerField('fields', validators=[NumberRange(min=0, max=None)], default=0)
    mills = IntegerField('mills', validators=[NumberRange(min=0, max=None)], default=0)
    mines = IntegerField('mines', validators=[NumberRange(min=0, max=None)], default=0)

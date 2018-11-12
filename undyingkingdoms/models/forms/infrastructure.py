from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import NumberRange


class InfrastructureForm(FlaskForm):
    house = IntegerField('house', validators=[NumberRange(min=0, max=None)], default=0)
    field = IntegerField('field', validators=[NumberRange(min=0, max=None)], default=0)
    mill = IntegerField('mill', validators=[NumberRange(min=0, max=None)], default=0)
    mine = IntegerField('mine', validators=[NumberRange(min=0, max=None)], default=0)

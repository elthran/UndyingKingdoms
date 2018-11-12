from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField
from wtforms.validators import NumberRange


class EconomyForm(FlaskForm):
    tax = SelectField('Tax', coerce=int)


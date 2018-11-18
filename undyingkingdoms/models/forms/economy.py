from flask_wtf import FlaskForm
from wtforms import SelectField


class EconomyForm(FlaskForm):
    tax = SelectField('Tax', coerce=int)
    rations = SelectField('Rations', coerce=str)


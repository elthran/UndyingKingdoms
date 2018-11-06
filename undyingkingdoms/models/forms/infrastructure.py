from flask_wtf import FlaskForm
from wtforms import IntegerField, HiddenField, Form
from wtforms.validators import NumberRange

from undyingkingdoms.static.metadata import all_buildings


class InfrastructureForm(FlaskForm):
    #summed_value = HiddenField("summed_value")
    pass


for name, amount, cost, maintenance, description in all_buildings:
    setattr(InfrastructureForm, name, IntegerField(name.title(), validators=[NumberRange(min=0, max=None)], default=0))

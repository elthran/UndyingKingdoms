from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import NumberRange

from undyingkingdoms.static.metadata import all_buildings


class InfrastructureForm(FlaskForm):
    # current_land = hidden_field
    pass


for name, amount, cost, maintenance, description in all_buildings:
    setattr(InfrastructureForm, name, IntegerField(name.title(), validators=[NumberRange(min=0, max=None)], default=0))

from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import NumberRange

from undyingkingdoms.static.metadata import all_armies


class AttackForm(FlaskForm):
    pass


for name, amount, attack, defence, health in all_armies:
    setattr(AttackForm, name, IntegerField(name.title(), validators=[NumberRange(min=0, max=None)], default=0))

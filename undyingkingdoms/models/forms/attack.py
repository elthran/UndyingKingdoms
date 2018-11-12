from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import NumberRange

from undyingkingdoms.static.metadata import all_armies


class AttackForm(FlaskForm):
    pass

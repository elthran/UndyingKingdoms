from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField
from wtforms.validators import NumberRange

from undyingkingdoms.static.metadata import all_armies


class AttackForm(FlaskForm):
    peasant = SelectField('peasant', coerce=int)
    archer = SelectField('archer', coerce=int)
    soldier = SelectField('soldier', coerce=int)
    elite = SelectField('elite', coerce=int)

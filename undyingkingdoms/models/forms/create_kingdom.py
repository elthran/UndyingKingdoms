from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from wtforms.validators import DataRequired, Email


class CreateKingdomForm(FlaskForm):
    name = StringField('Name')

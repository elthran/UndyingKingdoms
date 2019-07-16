from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from wtforms.validators import DataRequired, Email


class EmailVerificationForm(FlaskForm):
    code = PasswordField('Code', validators=[DataRequired(message='Must provide a code.')])

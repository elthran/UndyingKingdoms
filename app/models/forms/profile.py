from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from wtforms.validators import DataRequired, Email


class ProfileSecurityForm(FlaskForm):
    old_password = PasswordField('old_password', validators=[DataRequired(message='Must provide a password.')])
    new_password = PasswordField('new_password', validators=[DataRequired(message='Must provide a password.')])
    retype_new_password = PasswordField('retype_new_password', validators=[DataRequired(message='Must provide a password.')])

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.passwords_match():
            return False
        return True

    def passwords_match(self):
        if self.new_password.data != self.retype_new_password.data:
            return True


class ProfileEmailForm(FlaskForm):
    email = StringField('Email Address', validators=[Email(), DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password', validators=[DataRequired(message='Must provide a password.')])
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from wtforms.validators import DataRequired, Length, ValidationError

MAX_WORD_LEN = 24

class CreateKingdomForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message="You must provide a kingdom name."),
        Length(min=1, max=100),
    ])

    def validate_name(form, field):
        if any(len(word) > MAX_WORD_LEN for word in field.data.split()):
            raise ValidationError(f'No word can be longer than {MAX_WORD_LEN} characters')

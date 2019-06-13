from flask_wtf import FlaskForm
from wtforms import StringField

from wtforms.validators import DataRequired, Length, ValidationError

from undyingkingdoms.models.kingdoms import Kingdom

MAX_WORD_LEN = 24


class CreateKingdomForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message="You must provide a kingdom name."),
        Length(min=1, max=100),
    ])

    def validate_name(form, field):
        if any(len(word) > MAX_WORD_LEN for word in field.data.split()):
            raise ValidationError(f'No word can be longer than {MAX_WORD_LEN} characters')
        if Kingdom.query.filter_by(name=form.name.data).first():
            raise ValidationError(f'That clan name already exists')

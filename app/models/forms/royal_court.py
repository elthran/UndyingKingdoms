from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired, Length


class RoyalCourtMessageForm(FlaskForm):
    content = StringField('Content', validators=[DataRequired(message='Your post requires a message.')])


class RoyalCourtRelationsForm(FlaskForm):
    target_id = SelectField('Target', coerce=int)


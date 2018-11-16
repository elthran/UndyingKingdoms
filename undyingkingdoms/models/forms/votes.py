from flask_wtf import FlaskForm
from wtforms import SelectField


class VoteForm(FlaskForm):
    vote = SelectField('Vote', coerce=int)


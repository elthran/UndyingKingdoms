from flask_wtf import FlaskForm
from wtforms import SelectField


class TechnologyForm(FlaskForm):
    technology = SelectField('Technology', coerce=int)

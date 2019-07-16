from flask_wtf import FlaskForm
from wtforms import StringField, SelectField

from wtforms.validators import DataRequired, NoneOf, Length

from app.models.exports import County


class InitializeForm(FlaskForm):
    county = StringField('County', validators=[DataRequired(message='You must enter a name for your county.'),
                                               Length(min=2, max=20)])
    leader = StringField('Leader', validators=[DataRequired(message='You must enter a name for your leader.'),
                                               Length(min=2, max=20)])
    title = SelectField('Title', coerce=int, validators=[NoneOf([0], message='Must choose title.')])
    race = SelectField('Race', coerce=int, validators=[NoneOf([0], message='Must choose race.')])
    background = SelectField('Background', coerce=int, validators=[NoneOf([0], message='Must choose background.')])
    clan = SelectField('Clan', coerce=int)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.county_name_unique():
            return False
        return True

    def county_name_unique(self):
        existing_county = County.query.filter_by(name=self.county.data).first()
        if existing_county:
            self.county.errors.append("A county already exists by that name.")
            return True



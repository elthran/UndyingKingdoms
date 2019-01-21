from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField

from undyingkingdoms.models import County


class InfiltrateForm(FlaskForm):
    county_id = IntegerField('county_id')
    amount = SelectField('amount', coerce=int)
    mission = SelectField('mission', coerce=int)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.quantity_of_thieves():
            return False
        return True

    def quantity_of_thieves(self):
        county = County.query.filter_by(id=self.county_id.data).first()
        thieves_available = county.get_number_of_available_thieves()
        thieves_being_sent = self.amount.data
        if thieves_being_sent > thieves_available:
            self.amount.errors.append("You do not have enough thieves available.")
            return True
        if thieves_being_sent < 1:
            self.amount.errors.append("You must send at least one thief.")
            return True

from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField

from undyingkingdoms.models.exports import County
from undyingkingdoms.metadata.metadata import amount_of_thieves_modifier


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
        county = County.query.get(self.county_id.data)
        thieves_available = county.get_number_of_available_thieves()
        thieves_being_sent = self.amount.data
        maximum_per_mission = 3 + amount_of_thieves_modifier.get(county.race, ("", 0))[1] + amount_of_thieves_modifier.get(county.background, ("", 0))[1]
        if thieves_being_sent > thieves_available:
            self.amount.errors.append("You do not have enough thieves available.")
            return True
        if thieves_being_sent < 1:
            self.amount.errors.append("You must send at least one thief.")
            return True
        if thieves_being_sent > maximum_per_mission:
            self.amount.errors.append(f"You can not send more than {maximum_per_mission} thieves at a time.")
            return True

from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, HiddenField

from undyingkingdoms.models.counties.counties import County


class MerchantForm(FlaskForm):
    county_id = IntegerField('county_id')
    offer_resource = SelectField('offer_resource', coerce=int)
    offer = SelectField('offer', coerce=int)
    receive_resource = SelectField('receive_resource', coerce=int)
    receive = HiddenField('receive')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.empty_offer():
            return False
        if self.insufficient_funds():
            return False
        return True

    def empty_offer(self):
        if self.offer.data != 0:
                return False
        self.offer_resource.errors.append("You must offer something")
        return True

    def insufficient_funds(self):
        resource_map = {0: 'stone', 1: 'iron', 2: 'wood', 3: 'gold', 4: 'grain_stores'}
        county = County.query.get(self.county_id.data)
        resource_amount = getattr(county, resource_map[self.offer_resource.data])
        if resource_amount < self.offer.data:
            self.offer_resource.errors.append("You don't have enough {}".format(self.offer_resource.data))
            return True

from flask_wtf import FlaskForm
from wtforms import SelectField

from undyingkingdoms.models.counties.counties import County


class MerchantForm(FlaskForm):
    offer_resource = SelectField('offer_resource', coerce=int)
    offer = SelectField('offer', coerce=int)
    receive_resource = SelectField('receive_resource', coerce=int)
    receive = SelectField('receive', coerce=int)

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
        county = County.query.get(self.county_id.data)
        resource = getattr(county, self.offer_resource.data)
        if resource < self.data.offer:
            self.offer_resource.errors.append("You don't have enough {}".format(self.data.offer_resource))
            return True

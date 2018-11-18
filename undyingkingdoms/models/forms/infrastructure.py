from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import NumberRange

from undyingkingdoms.models.counties import County


class InfrastructureForm(FlaskForm):
    county_id = IntegerField('county_id')
    houses = IntegerField('houses', validators=[NumberRange(min=0, max=None)], default=0)
    fields = IntegerField('fields', validators=[NumberRange(min=0, max=None)], default=0)
    mills = IntegerField('mills', validators=[NumberRange(min=0, max=None)], default=0)
    mines = IntegerField('mines', validators=[NumberRange(min=0, max=None)], default=0)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.insufficient_gold():
            return False
        if self.insufficient_wood():
            return False
        return True

    def insufficient_gold(self):
        gold_cost = 0
        county = County.query.filter_by(id=self.county_id.data).first()
        for building in [self.houses, self.fields, self.mills, self.mines]:
            gold_cost += county.buildings[building.name].gold * building.data
        if gold_cost > county.gold:
            self.county_id.errors.append("Not enough gold.")
            return True

    def insufficient_wood(self):
        wood_cost = 0
        county = County.query.filter_by(id=self.county_id.data).first()
        for building in [self.houses, self.fields, self.mills, self.mines]:
            wood_cost += county.buildings[building.name].wood * building.data
        if wood_cost > county.wood:
            self.county_id.errors.append("Not enough wood.")
            return True

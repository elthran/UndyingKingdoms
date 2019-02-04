from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import NumberRange

from undyingkingdoms.models.counties import County


class InfrastructureForm(FlaskForm):
    county_id = IntegerField('county_id')
    house = IntegerField('house', validators=[NumberRange(min=0, max=None)], default=0)
    field = IntegerField('field', validators=[NumberRange(min=0, max=None)], default=0)
    pasture = IntegerField('pasture', validators=[NumberRange(min=0, max=None)], default=0)
    mill = IntegerField('mill', validators=[NumberRange(min=0, max=None)], default=0)
    mine = IntegerField('mine', validators=[NumberRange(min=0, max=None)], default=0)
    fort = IntegerField('fort', validators=[NumberRange(min=0, max=None)], default=0)
    stables = IntegerField('stables', validators=[NumberRange(min=0, max=None)], default=0)
    guild = IntegerField('guild', validators=[NumberRange(min=0, max=None)], default=0)
    bank = IntegerField('bank', validators=[NumberRange(min=0, max=None)], default=0)
    lair = IntegerField('lair', validators=[NumberRange(min=0, max=None)], default=0)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.insufficient_gold():
            return False
        if self.insufficient_wood():
            return False
        if self.insufficient_land():
            return False
        return True

    def insufficient_gold(self):
        gold_cost = 0
        county = County.query.filter_by(id=self.county_id.data).first()
        for building in [self.house, self.field, self.pasture, self.mill, self.mine, self.fort, self.stables, self.guild, self.bank, self.lair]:
            gold_cost += county.buildings[building.name].gold * building.data
        if gold_cost > county.gold:
            self.county_id.errors.append("Not enough gold.")
            return True

    def insufficient_wood(self):
        wood_cost = 0
        county = County.query.filter_by(id=self.county_id.data).first()
        for building in [self.house, self.field, self.pasture, self.mill, self.mine, self.fort, self.stables, self.guild, self.bank, self.lair]:
            wood_cost += county.buildings[building.name].wood * building.data
        if wood_cost > county.wood:
            self.county_id.errors.append("Not enough wood.")
            return True

    def insufficient_land(self):
        land_cost = 0
        county = County.query.filter_by(id=self.county_id.data).first()
        for building in [self.house, self.field, self.pasture, self.mill, self.mine, self.fort, self.stables, self.guild, self.bank, self.lair]:
            land_cost += building.data
        if land_cost > county.get_available_land():
            self.county_id.errors.append("Not enough land.")
            return True

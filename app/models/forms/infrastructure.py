from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField
from wtforms.validators import NumberRange

from app.models.exports import County


class InfrastructureForm(FlaskForm):
    county_id = IntegerField('county_id')
    house = IntegerField('house', validators=[NumberRange(min=0, max=None)], default=0)
    field = IntegerField('field', validators=[NumberRange(min=0, max=None)], default=0)
    pasture = IntegerField('pasture', validators=[NumberRange(min=0, max=None)], default=0)
    mill = IntegerField('mill', validators=[NumberRange(min=0, max=None)], default=0)
    mine = IntegerField('mine', validators=[NumberRange(min=0, max=None)], default=0)
    quarry = IntegerField('quarry', validators=[NumberRange(min=0, max=None)], default=0)
    fort = IntegerField('fort', validators=[NumberRange(min=0, max=None)], default=0)
    stables = IntegerField('stables', validators=[NumberRange(min=0, max=None)], default=0)
    bank = IntegerField('bank', validators=[NumberRange(min=0, max=None)], default=0)
    tavern = IntegerField('tavern', validators=[NumberRange(min=0, max=None)], default=0)
    tower = IntegerField('tower', validators=[NumberRange(min=0, max=None)], default=0)
    lab = IntegerField('lab', validators=[NumberRange(min=0, max=None)], default=0)
    arcane = IntegerField('arcane', validators=[NumberRange(min=0, max=None)], default=0)
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
        county = County.query.get(self.county_id.data)
        infrastructure = county.infrastructure
        for building in [self.house, self.field, self.pasture, self.mill, self.mine, self.quarry, self.fort,
                         self.stables, self.bank, self.tavern, self.tower, self.lab, self.arcane, self.lair]:
            gold_cost += infrastructure.buildings[building.name].gold_cost * building.data
        if gold_cost > county.gold:
            self.county_id.errors.append("Not enough gold.")
            return True

    def insufficient_wood(self):
        wood_cost = 0
        county = County.query.get(self.county_id.data)
        infrastructure = county.infrastructure
        for building in [self.house, self.field, self.pasture, self.mill, self.mine, self.quarry, self.fort,
                         self.stables, self.bank, self.tavern, self.tower, self.lab, self.arcane, self.lair]:
            wood_cost += infrastructure.buildings[building.name].wood_cost * building.data
        if wood_cost > county.wood:
            self.county_id.errors.append("Not enough wood.")
            return True

    def insufficient_stone(self):
        stone_cost = 0
        county = County.query.filter_by(id=self.county_id.data).first()
        infrastructure = county.infrastructure
        for building in [self.house, self.field, self.pasture, self.mill, self.mine, self.quarry, self.fort,
                         self.stables, self.bank, self.tavern, self.tower, self.lab, self.arcane, self.lair]:
            stone_cost += infrastructure.buildings[building.name].stone_cost * building.data
        if stone_cost > county.stone:
            self.county_id.errors.append("Not enough stone.")
            return True

    def insufficient_land(self):
        land_cost = 0
        county = County.query.get(self.county_id.data)
        infrastructure = county.infrastructure
        for building in [self.house, self.field, self.pasture, self.mill, self.mine, self.quarry, self.fort,
                         self.stables, self.bank, self.tavern, self.tower, self.lab, self.arcane, self.lair]:
            land_cost += building.data
        if land_cost > infrastructure.get_available_land():
            self.county_id.errors.append("Not enough land.")
            return True


class ExcessProductionForm(FlaskForm):
    goal = SelectField('Goal', coerce=int)

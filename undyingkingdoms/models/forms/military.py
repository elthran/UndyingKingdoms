from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import NumberRange

from undyingkingdoms.models.exports import County


class MilitaryForm(FlaskForm):
    county_id = IntegerField('county_id')
    peasant = IntegerField('peasant', validators=[NumberRange(min=0, max=None)], default=0)
    archer = IntegerField('archer', validators=[NumberRange(min=0, max=None)], default=0)
    soldier = IntegerField('soldier', validators=[NumberRange(min=0, max=None)], default=0)
    besieger = IntegerField('besieger', validators=[NumberRange(min=0, max=None)], default=0)
    summon = IntegerField('summon', validators=[NumberRange(min=0, max=None)], default=0)
    elite = IntegerField('elite', validators=[NumberRange(min=0, max=None)], default=0)
    monster = IntegerField('monster', validators=[NumberRange(min=0, max=None)], default=0)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.insufficient_gold():
            return False
        if self.insufficient_wood():
            return False
        if self.insufficient_iron():
            return False
        if self.insufficient_lairs():
            return False
        if self.insufficient_population():
            return False
        return True

    def insufficient_gold(self):
        gold_cost = 0
        county = County.query.get(self.county_id.data)
        for army in [self.peasant, self.archer, self.soldier, self.besieger, self.summon, self.elite, self.monster]:
            gold_cost += county.armies[army.name].gold * army.data
        if gold_cost > county.gold:
            self.county_id.errors.append("Not enough gold.")
            return True

    def insufficient_wood(self):
        wood_cost = 0
        county = County.query.get(self.county_id.data)
        for army in [self.peasant, self.archer, self.soldier, self.besieger, self.summon, self.elite, self.monster]:
            wood_cost += county.armies[army.name].wood * army.data
        if wood_cost > county.wood:
            self.county_id.errors.append("Not enough wood.")
            return True

    def insufficient_iron(self):
        iron_cost = 0
        county = County.query.get(self.county_id.data)
        for army in [self.peasant, self.archer, self.soldier, self.besieger, self.summon, self.elite, self.monster]:
            iron_cost += county.armies[army.name].iron * army.data
        if iron_cost > county.iron:
            self.county_id.errors.append("Not enough iron.")
            return True

    def insufficient_lairs(self):
        county = County.query.get(self.county_id.data)
        max_monsters = county.buildings['lair'].total * county.buildings['lair'].output
        current_monsters = county.armies['monster'].total + county.armies['monster'].currently_training
        available = max_monsters - current_monsters
        if self.monster.data > available:
            self.county_id.errors.append(f"Not enough {county.buildings['lair'].class_name}.")
            return True
        
    def insufficient_population(self):
        county = County.query.get(self.county_id.data)
        available_population = county.get_available_workers()
        required_population = 0
        for army in [self.peasant, self.archer, self.soldier, self.besieger, self.summon, self.elite, self.monster]:
            required_population += army.data
        if required_population > available_population:
            self.county_id.errors.append("Not enough people are available.")
            return True



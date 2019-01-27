from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange

from undyingkingdoms.models.counties import County


class MilitaryForm(FlaskForm):
    county_id = IntegerField('county_id')
    peasant = IntegerField('peasant', validators=[NumberRange(min=0, max=None)], default=0)
    archer = IntegerField('archer', validators=[NumberRange(min=0, max=None)], default=0)
    soldier = IntegerField('soldier', validators=[NumberRange(min=0, max=None)], default=0)
    elite = IntegerField('elite', validators=[NumberRange(min=0, max=None)], default=0)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.insufficient_gold():
            return False
        if self.insufficient_wood():
            return False
        if self.insufficient_iron():
            return False
        return True

    def insufficient_gold(self):
        gold_cost = 0
        county = County.query.filter_by(id=self.county_id.data).first()
        for army in [self.peasant, self.archer, self.soldier, self.elite]:
            gold_cost += county.armies[army.name].gold * army.data
        if gold_cost > county.gold:
            self.county_id.errors.append("Not enough gold.")
            return True

    def insufficient_wood(self):
        wood_cost = 0
        county = County.query.filter_by(id=self.county_id.data).first()
        for army in [self.peasant, self.archer, self.soldier, self.elite]:
            wood_cost += county.armies[army.name].wood * army.data
        if wood_cost > county.wood:
            self.county_id.errors.append("Not enough wood.")
            return True

    def insufficient_iron(self):
        iron_cost = 0
        county = County.query.filter_by(id=self.county_id.data).first()
        for army in [self.peasant, self.archer, self.soldier, self.elite]:
            iron_cost += county.armies[army.name].iron * army.data
        if iron_cost > county.iron:
            self.county_id.errors.append("Not enough iron.")
            return True



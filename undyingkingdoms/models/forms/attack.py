from flask_wtf import FlaskForm
from wtforms import SelectField


class AttackForm(FlaskForm):
    peasant = SelectField('peasant', coerce=int)
    soldier = SelectField('soldier', coerce=int)
    besieger = SelectField('besieger', coerce=int)
    summon = SelectField('summon', coerce=int)
    elite = SelectField('elite', coerce=int)
    monster = SelectField('monster', coerce=int)
    
    attack_type = SelectField('attack_type', coerce=str)

    def __init__(self, county=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.county = county
        self.army = None

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.insufficient_strength():
            return False
        return True

    def insufficient_strength(self):
        """Calculates army strength.

        Adds army object to form.
        """
        army = {}
        units = (unit for unit in self.county.armies.values() if unit.name not in ['archer'])
        for unit in units:
            if self.data[unit.name] > unit.total:
                return True
            army[unit.name] = self.data[unit.name]
        strength = self.county.get_offensive_strength(army=army)
        if strength < 150:
            self.peasant.errors.append(f"Must send troops worth at least 150 strength "
                                       f"(sent troops worth {strength} strength).")
            return True
        self.army = army
        return False

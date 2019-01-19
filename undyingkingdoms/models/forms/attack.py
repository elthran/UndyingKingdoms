from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField

from undyingkingdoms.models.counties import County


class AttackForm(FlaskForm):
    peasant = SelectField('peasant', coerce=int)
    archer = SelectField('archer', coerce=int)
    soldier = SelectField('soldier', coerce=int)
    elite = SelectField('elite', coerce=int)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.insufficient_troops():
            return False
        return True

    def insufficient_troops(self):
        troops_being_sent = self.peasant.data + self.archer.data + self.soldier.data + self.elite.data
        if troops_being_sent < 25:
            self.soldier.errors.append("Must send at least 25 troops.")
            return True


class TempGameAdvance(FlaskForm):
    pass

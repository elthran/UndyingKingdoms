from flask_wtf import FlaskForm
from wtforms import SelectField


class AttackForm(FlaskForm):
    peasant = SelectField('peasant', coerce=int)
    soldier = SelectField('soldier', coerce=int)
    elite = SelectField('elite', coerce=int)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.insufficient_troops():
            return False
        return True

    def insufficient_troops(self):
        troops_being_sent = self.peasant.data + self.soldier.data + self.elite.data
        if troops_being_sent < 25:
            self.peasant.errors.append("Must send at least 25 troops.")
            self.soldier.errors.append("Must send at least 25 troops.")
            self.elite.errors.append("Must send at least 25 troops.")
            return True

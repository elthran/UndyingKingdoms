from flask_wtf import FlaskForm
from wtforms import SelectField


class TradeForm(FlaskForm):
    offer_gold = SelectField('offer_gold', coerce=int)
    offer_wood = SelectField('offer_wood', coerce=int)
    offer_iron = SelectField('offer_iron', coerce=int)
    offer_stone = SelectField('offer_stone', coerce=int)

    receive_gold = SelectField('receive_gold', coerce=int)
    receive_wood = SelectField('receive_wood', coerce=int)
    receive_iron = SelectField('receive_iron', coerce=int)
    receive_stone = SelectField('receive_stone', coerce=int)

    duration = SelectField('duration', coerce=int)  # How long they have to accept

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.empty_offer():
            return False
        return True

    def empty_offer(self):
        for item in [self.offer_gold, self.offer_wood, self.offer_iron, self.offer_stone,
                     self.receive_gold, self.receive_wood, self.receive_iron, self.receive_wood]:
            if item.data != 0:
                return False
        self.offer_gold.errors.append("You must offer or request something")
        return True

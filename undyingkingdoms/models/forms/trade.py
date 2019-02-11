from flask_wtf import FlaskForm
from wtforms import SelectField


class TradeForm(FlaskForm):
    offer_gold = SelectField('offer_gold', coerce=int)
    offer_wood = SelectField('offer_wood', coerce=int)
    offer_iron = SelectField('offer_iron', coerce=int)

    receive_gold = SelectField('receive_gold', coerce=int)
    receive_wood = SelectField('receive_wood', coerce=int)
    receive_iron = SelectField('receive_iron', coerce=int)



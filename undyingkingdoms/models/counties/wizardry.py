from random import choice

from sqlalchemy.ext.hybrid import hybrid_property

from undyingkingdoms.models.magic import Casting
from undyingkingdoms.models.notifications import Notification
from ..bases import GameState, db


class Wizardry(GameState):
    max_mana = db.Column(db.Integer)
    _mana_change = db.Column(db.Integer)
    recoup_factor = db.Column(db.Integer)

    @hybrid_property
    def mana_change(self):
        county = self.county

        growth = self._mana_change
        active_spells = Casting.query.filter_by(county_id=county.id).filter_by(active=True).all()
        loss = sum(spell.mana_sustain for spell in active_spells)
        difference = int(growth - loss)
        if difference < 0 and county.mana + difference < 0:
            drop_spell = choice(active_spells)
            drop_spell.active = False
            drop_spell.save()  # might be unneeded
            notice = Notification(
                county,
                "Spell Ended",
                f"You did not have enough mana and {drop_spell.name} ended.",
                "Spell End"
            )
            notice.save()
            # noinspection PyPropertyAccess
            return self.mana_change
        return difference

    @mana_change.setter
    def mana_change(self, value):
        self._mana_change = value

    # noinspection PyUnresolvedReferences
    @mana_change.expression
    def mana_change(self):
        return self._mana_change

    def __init__(self, county):
        self.county = county
        self.max_mana = 20
        self.mana_change = 2
        self.recoup_factor = 0

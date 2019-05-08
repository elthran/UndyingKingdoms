from sqlalchemy.ext.hybrid import hybrid_property

from undyingkingdoms.metadata.metadata import offensive_power_modifier
from ..magic import Casting
from ..helpers import compute_modifier
from ..bases import GameState, db


class Military(GameState):
    _offensive_modifier = db.Column(db.Float)
    _offensive_power = db.Column(db.Integer)

    @hybrid_property
    def offensive_modifier(self):
        modify_offensive_power = Casting.query.filter_by(target_id=self.id, name="modify_offensive_power").filter(
            (Casting.duration > 0) | (Casting.active == True)).all()
        spell_modifier = 0
        for spell in modify_offensive_power or []:
            spell_modifier += spell.output * self.spell_modifier

        return spell_modifier + self._offensive_modifier

    @offensive_modifier.setter
    def offensive_modifier(self, value):
        self._offensive_modifier = value

    @hybrid_property
    def offensive_power(self, army=None, scoreboard=False, enemy_forts=0):
        """Returns the attack power of your army or subset of your army.

        If no army is sent in, it checks the full potential of the county.
        params: scoreboard - Looks at total possible power, even for troops who are unavailable

        To pass args use:
        Military.offensive_power.fget(county, *args, **kwargs)

        NOTE: offensive power can only be calculated for _this_ county.
        """
        strength = 0
        if army:
            for unit in army.values():
                if unit.name == 'besieger':
                    strength += unit.name * enemy_forts * max(unit.attack, 1)
                elif unit.attack > 0:
                    strength += unit.name * unit.attack
        else:
            for unit in self.armies.values():
                if scoreboard:
                    strength += unit.total * unit.attack
                else:
                    strength += unit.available * unit.attack
        # noinspection PyPropertyAccess
        return (strength + self._offensive_power) * self.offensive_modifier

    @offensive_power.setter
    def offensive_power(self, value):
        self._offensive_power = value

    def __init__(self, county):
        self.county = county
        self._offensive_modifier = 1 + compute_modifier(offensive_power_modifier, county.race, county.background)
        self._offensive_power = 0

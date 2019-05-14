from sqlalchemy.ext.hybrid import hybrid_property

from undyingkingdoms.metadata.metadata import offensive_power_modifier
from ..magic import Casting
from ..helpers import compute_modifier
from ..bases import GameState, db


class Military(GameState):
    BASE_DURATION = {'Attack': 18, 'Pillage': 12, 'Raze': 8}

    _offensive_modifier = db.Column(db.Float)
    _offensive_power = db.Column(db.Integer)
    _speed_modifier = db.Column(db.Float)
    speed = db.Column(db.Integer)
    _unit_health = db.Column(db.Integer)
    _non_siege_health = db.Column(db.Integer)
    _unit_upkeep = db.Column(db.Integer)

    @hybrid_property
    def offensive_modifier(self):
        county = self.county
        modify_offensive_power = Casting.query.filter_by(target_id=county.id, name="modify_offensive_power").filter(
            (Casting.duration > 0) | (Casting.active == True)).all()
        spell_modifier = 0
        for spell in modify_offensive_power or []:
            spell_modifier += spell.output * county.spell_modifier

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
        Military.offensive_power.fget(county.military, *args, **kwargs)

        NOTE: offensive power can only be calculated for _this_ county.
        """
        assert type(self) == Military

        county = self.county
        strength = 0
        if army:
            for unit in county.armies.values():
                if unit.type == unit.BESIEGER:
                    strength += army[unit.name] * enemy_forts * max(unit.attack, 1)
                elif unit.attack > 0:
                    strength += army[unit.name] * unit.attack
        else:
            for unit in county.armies.values():
                if scoreboard:
                    strength += unit.total * unit.attack
                else:
                    strength += unit.available * unit.attack
        # noinspection PyPropertyAccess
        return round(
            (strength + self._offensive_power)
            * self.offensive_modifier
        )

    @offensive_power.setter
    def offensive_power(self, value):
        self._offensive_power = value

    # noinspection PyUnresolvedReferences
    @offensive_power.expression
    def offensive_power(cls):
        """Allow queries on offensive power.

        if no "prop.expression" exists you need to use
        `Military.__dict__['offensive_power'].fget(self, *args, **kwargs)`
        """
        # warnings.warn("undyingkingdoms.models.counties.military.Military#offensive_power: querying isn't really implemented.", UserWarning)
        return cls._offensive_power

    @hybrid_property
    def speed_modifier(self):
        county = self.county
        speed_modifier = self._speed_modifier
        speed_modifier += (county.buildings['stables'].total ** 0.9) * 100 * county.buildings['stables'].output / county.land
        return speed_modifier

    @speed_modifier.setter
    def speed_modifier(self, value):
        self._speed_modifier = value

    # noinspection PyUnresolvedReferences
    @speed_modifier.expression
    def speed_modifier(self):
        return self._speed_modifier

    @hybrid_property
    def unit_health(self):
        return self._unit_health

    @unit_health.setter
    def unit_health(self, value):
        county = self.county
        for unit in county.armies.values():
            # noinspection PyPropertyAccess
            unit.health += value - (self.unit_health or 0)
        self._unit_health = value

    @hybrid_property
    def non_siege_health(self):
        return self._non_siege_health

    @non_siege_health.setter
    def non_siege_health(self, value):
        county = self.county
        for unit in county.armies.values():
            # all non-siege units.
            if unit.type != unit.BESIEGER:
                # noinspection PyPropertyAccess
                unit.health += value - (self.non_siege_health or 0)
        self._non_siege_health = value

    @hybrid_property
    def unit_upkeep(self):
        return self._unit_upkeep

    @unit_upkeep.setter
    def unit_upkeep(self, value):
        county = self.county
        for unit in county.armies.values():
            # noinspection PyPropertyAccess
            unit.upkeep += value - (self.unit_upkeep or 0)
        self._unit_upkeep = value

    def get_expedition_duration(self, attack_type, successful):
        # noinspection PyPropertyAccess
        duration = self.BASE_DURATION[attack_type] * 100 / self.speed_modifier
        duration -= self.speed
        if not successful:
            duration *= 0.5
        return round(max(duration, 3))

    def __init__(self, county):
        self.county = county
        self.offensive_modifier = 1 + compute_modifier(offensive_power_modifier, county.race, county.background)
        self.offensive_power = 0
        self.speed_modifier = 100
        self.speed = 0
        self.unit_health = 0
        self.non_siege_health = 0
        self.unit_upkeep = 0

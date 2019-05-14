from sqlalchemy.ext.hybrid import hybrid_property

from tests import bp
from undyingkingdoms.metadata.metadata import offensive_power_modifier
from undyingkingdoms.models.armies import Army
from ..magic import Casting
from ..helpers import compute_modifier
from ..bases import GameState, db


class Military(GameState):
    BASE_DURATION = {'Attack': 18, 'Pillage': 12, 'Raze': 8}
    FILTERS = set(Army.TYPES.keys()) | {"unit", 'non_siege'}

    _offensive_modifier = db.Column(db.Float)
    _offensive_power = db.Column(db.Integer)
    _speed_modifier = db.Column(db.Float)
    speed = db.Column(db.Integer)
    unit_health = db.Column(db.Integer)
    non_siege_health = db.Column(db.Integer)
    unit_upkeep = db.Column(db.Integer)
    archer_defence = db.Column(db.Integer)

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

    def __setattr__(self, key, value):
        """Implement custom quick set to unit attribute.

        self.archer_defence = 1 should now mutate your archers defence.
        Eventually I'd like to add in the filters from the
        get_modifiers() code.
        """
        try:
            filter, unit_attr = key.rsplit('_', maxsplit=1)
        except ValueError:
            filter = None
            unit_attr = None
        # I might need to check if there is a custom setter as well?
        if filter in self.FILTERS:
            county = self.county
            # I probably can make this one if ... but I was having
            # some boolean logic trouble making non_siege short circuiting.
            for unit in county.armies.values():
                if filter in 'unit':
                    self.set_unit_attribute(unit, key, unit_attr, value)
                elif filter == 'non_siege':
                    if unit.type != unit.BESIEGER:
                        self.set_unit_attribute(unit, key, unit_attr, value)
                elif  unit.type == unit.TYPES[filter]:
                    self.set_unit_attribute(unit, key, unit_attr, value)
        super().__setattr__(key, value)

    def set_unit_attribute(self, unit, key, attr, value):
        """Modify the attribute of a unit by specific modifier."""
        unit_val = getattr(unit, attr)
        setattr(
            unit,
            attr,
            unit_val + value - (getattr(self, key) or 0)
        )

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
        self.archer_defence = 0

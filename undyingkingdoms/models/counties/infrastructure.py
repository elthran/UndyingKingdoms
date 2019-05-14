from sqlalchemy.ext.hybrid import hybrid_property

from ..bases import GameState, db


class Infrastructure(GameState):
    _cost_modifier = db.Column(db.Float)
    _fort_multiplier = db.Column(db.Float)

    @hybrid_property
    def cost_modifier(self):
        return self._cost_modifier

    # noinspection PyPropertyAccess
    @cost_modifier.setter
    def cost_modifier(self, value):
        county = self.county
        for building in county.buildings.values():
            building.gold_cost *= value - (self.cost_modifier or 0)
            building.wood_cost *= value - (self.cost_modifier or 0)
            building.stone_cost *= value - (self.cost_modifier or 0)
        self._cost_modifier = value

    @hybrid_property
    def fort_multiplier(self):
        return self._fort_multiplier

    @fort_multiplier.setter
    def fort_multiplier(self, value):
        """Increase the productivity of forts.

        This is a bit of an odd one.
        fort_multiplier == 0 would make forts useless.
        fort_multiplier < 1 would reduce fort effectiveness.

        To increase for effectiveness by 20% you would do
        fort_multiplier = 1.2

        I feel that this is the most transparent and flexible way to do this
        although it follows a completely different pattern than all other effects.
        """
        county = self.county
        fort = county.buildings['fort']
        # noinspection PyPropertyAccess
        fort.output *= value - (self.fort_multiplier or 0)
        self._fort_multiplier = value

    def __init__(self, county):
        self.county = county
        self.cost_modifier = 0
        self.fort_multiplier = 1

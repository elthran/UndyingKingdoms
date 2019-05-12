from ..bases import GameState, db


class Wizardry(GameState):
    max_mana = db.Column(db.Integer)

    def __init__(self, county):
        self.county = county
        self.max_mana = 20

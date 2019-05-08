from ..bases import GameState


class Military(GameState):
    def __init__(self, county):
        self.county = county

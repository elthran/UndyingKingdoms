from .bases import GameEvent, db


class Tutorial(GameEvent):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(32))
    current_step = db.Column(db.Integer)
    total_steps = db.Column(db.Integer)
    cancelled = db.Column(db.Boolean)

    def __init__(self, user_id, name, total_steps):
        self.user_id = user_id
        self.name = name
        self.current_step = 0
        self.total_steps = total_steps
        self.cancelled = False

    def get_step_description(self):
        descriptions = {"ftue": {'0': "Change your tax rate",
                                 '1': "Build a building"}
                        }
        return descriptions[self.name][str(self.current_step)]

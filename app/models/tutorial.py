from .bases import GameEvent, db
from app.metadata.tutorials.economy_tutorial import descriptions


class Tutorial(GameEvent):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(32))
    advisor = db.Column(db.String(32))
    current_step = db.Column(db.Integer)
    total_steps = db.Column(db.Integer)
    completed = db.Column(db.Boolean)

    def __init__(self, user_id, name, advisor, total_steps):
        self.user_id = user_id
        self.name = name
        self.advisor = advisor
        self.current_step = 1
        self.total_steps = total_steps
        self.completed = False

    def advance_step(self, current_step):
        self.current_step = current_step + 1
        if self.current_step > self.total_steps:
            self.completed = True

    def is_clickable_step(self):
        return descriptions[self.name][self.current_step]["clickable"]

    def get_step_description(self, _=None):
        """
        Some descriptions are simple text to read. They can be clicked through.
        """

        return descriptions[self.name][self.current_step]["description"]

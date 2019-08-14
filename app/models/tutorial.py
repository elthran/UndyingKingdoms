from .bases import GameEvent, db


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
        self.current_step = 0
        self.total_steps = total_steps
        self.completed = False

    def advance_step(self, current_step):
        self.current_step = current_step + 1
        if self.current_step >= self.total_steps:
            self.completed = True

    def get_step_description(self, get_click=False):
        """
        Some descriptions are simple text to read. They can be clicked through.
        """
        descriptions = {
            "ftue":
                {
                    "0": {
                        "description": "Congratulations on rightfully taking your throne as ruler."
                                       " I am Xin Jiang, your economic advisor.",
                        "clickable": True
                    },
                    "1": {
                        "description": "As the new ruler, you should lower the enormous tax rate "
                                       "imposed by the previous leader. That will help ensure your"
                                       " people's contentment with you as ruler.",
                        "clickable": True
                    },
                    "2": {
                        "description": "Go to the 'Economist' page ",
                        "clickable": False
                    },
                    "3": {
                        "description": "Lower your tax rate.",
                        "clickable": False
                    }
                }
        }
        if get_click:
            return descriptions[self.name][str(self.current_step)]["clickable"]
        return descriptions[self.name][str(self.current_step)]["description"]

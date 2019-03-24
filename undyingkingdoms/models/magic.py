from undyingkingdoms.models.bases import GameEvent, db


class Magic(GameEvent):

    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    county_day = db.Column(db.Integer)
    name = db.Column(db.String(64))
    class_name = db.Column(db.String(64))
    category = db.Column(db.String(64))  # instant, timed, aura
    targets = db.Column(db.String(16))  # self, friendly, hostile, all
    known = db.Column(db.Boolean)
    mana_cost = db.Column(db.Integer)
    mana_sustain = db.Column(db.Integer)  # Mana required to spend each day to sustain the spell
    duration = db.Column(db.Integer)  # How many game days the spell lasts for
    output = db.Column(db.Integer)  # Sometimes used to weigh the power of the spell.
    description = db.Column(db.String(128))

    def __init__(self, name, class_name=None, category='instant', targets='self',
                 known=False, mana_cost=0, mana_sustain=0, duration=0, output=0,
                 description="Unknown"):

        self.name = name
        self.class_name = class_name
        if class_name is None:
            self.class_name = name
        self.category = category
        self.targets = targets
        self.known = known
        self.mana_cost = mana_cost
        self.mana_sustain = mana_sustain
        self.duration = duration
        self.output = output
        self.description = description

    @staticmethod
    def get_know_spells(county):
        return Magic.query.filter_by(county_id=county.id, known=True).all()

    @staticmethod
    def get_unknown_spells(county):
        return Magic.query.filter_by(county_id=county.id, known=False).all()

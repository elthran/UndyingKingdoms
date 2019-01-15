from undyingkingdoms.models.achievements import Achievement
from undyingkingdoms.models.counties import County
from undyingkingdoms.models.bases import GameState, db
from undyingkingdoms.static.metadata import kingdom_names


class Kingdom(GameState):
    name = db.Column(db.String(128), nullable=False, unique=True)
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'), nullable=False)
    counties = db.relationship('County', backref='kingdom')
    leader = db.Column(db.Integer)  # county.id of leader

    def __init__(self, name):
        self.name = name
        self.leader = 0
        self.world_id = 1

    def __repr__(self):
        return '<Kingdom %r (%r)>' % (self.name, self.id)

    def get_votes_needed(self):
        return max(len(self.counties) // 3, 3)

    def get_most_popular_county(self):
        counties = [(county.get_votes_for_self(), county) for county in self.counties]
        return max(counties, key=lambda x: x[0])[1]

    def count_votes(self):
        if self.get_most_popular_county().get_votes_for_self() >= self.get_votes_needed():
            county = self.get_most_popular_county()
            self.leader = county.id
            achievement = Achievement.query.filter_by(user_id=county.user_id, category="class_leader",
                                                      sub_category=county.race).first()
            achievement.current_tier += 1

    def get_leader_name(self, county_id):
        return County.query.filter_by(id=county_id).first().name

    def kingdom_button(self, direction, current_id):
        if direction == 'left':
            current_id -= 1
        elif direction == 'right':
            current_id += 1
        if current_id == 0:
            current_id = len(kingdom_names)
        elif current_id > len(kingdom_names):
            current_id = 1
        chosen_kingdom = Kingdom.quer.filter_by(id=current_id).first()  # Get the chosen kingdom
        if len(chosen_kingdom.counties) == 0:  # If it's empty, skip it and go to next kingdom in that direction
            return self.kingdom_button(direction, current_id)
        return current_id

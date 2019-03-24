from undyingkingdoms.models.bases import GameEvent, db

class Clan(GameEvent):
    kingdom_id = db.Column(db.Integer, db.ForeignKey('kingdom.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    is_owner = db.Column(db.Boolean)
    status = db.Column(db.String(16))

    STATUS_OPTIONS = ['Invited', 'Member', 'Declined', 'Quit']

    @property
    def invited(self):
        return self.get_user_by_status('Invited')

    @property
    def members(self):
        return self.get_user_by_status('Member')

    @property
    def declined(self):
        return self.get_user_by_status('Declined')

    @property
    def quit(self):
        return self.get_user_by_status('Quit')

    @property
    def owner(self):
        owner_entry = self.query.filter_by(kingdom_id=self.kingdom_id, is_owner=True).first()
        try:
            return owner_entry.user
        except AttributeError:
            return None

    @db.validates('is_owner')
    def validate_is_owner(self, key, value):
        if value:
            owner = self.owner
            if owner is not None:
                raise AttributeError(f"This clan already as an owner of {owner}")
        return value

    @db.validates('status')
    def validate_status(self, key, value):
        if value not in Clan.STATUS_OPTIONS:
            raise AttributeError(f'Status must be one of: {Clan.STATUS_OPTIONS}')
        return value

    def __init__(self, kingdom_id, user_id, is_owner=False, status="Invited"):
        """Create a new clan relationship between user and kingdom tables.

        Usage is:
            user.clan -> returns Clan object
            user.clan.kingdom -> returns Kingdom of clan
            user.clan.users -> returns a list of all users in clan
            user.clan.owner -> user who made clan
            user.clan.is_owner -> boolean, whether this user is the owner
        """
        self.kingdom_id = kingdom_id
        self.user_id = user_id
        self.is_owner = is_owner
        if is_owner:
            status = "Member"
        self.status = status


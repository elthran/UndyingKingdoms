from extensions import flask_db as db

def clan_addon(user_cls, clan_cls, kingdom_cls):
    """Modify User so as to add a relationship to the clan class."""

    user_cls.clan = db.relationship("Clan", backref='user', uselist=False)
    clan_cls.kingdom = db.relationship("Kingdom")


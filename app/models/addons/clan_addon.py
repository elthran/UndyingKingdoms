from extensions import flask_db as db


def clan_addon(user_cls, clan_cls, kingdom_cls):
    """Modify User so as to add a relationship to the clan class.

    Note: user.clan might be None even though clan.user would be a user.
    This occurs when clan status is anything other than "Member".
    """

    user_cls.clan = db.relationship(
        "Clan",
        primaryjoin=(
            "and_("
            "User.id==Clan.user_id, "
            "Clan.status=='Member'"
            ")"
        ),
        uselist=False)

    clan_cls.user = db.relationship("User")

    def get_user_by_status(self, option):
        """Return a list of users based on membership status.

        This should be a join query of some kind.
        """
        return (
            user_cls
            .query
            .join(clan_cls)
            .filter(clan_cls.kingdom_id==self.kingdom_id, clan_cls.status==option)
            .all()
        )

    clan_cls.get_user_by_status = get_user_by_status

    clan_cls.kingdom = db.relationship("Kingdom")


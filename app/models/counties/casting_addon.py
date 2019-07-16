from extensions import flask_db as db

active_condition = (
    "or_(casting.c.duration > 0, casting.c.active==True)"
)

def casting_addon(cls):
    """Modify County so as to add a relationship to the casting class.

    Casting.query.filter_by(target_id=current_user.county.id).filter((Casting.duration > 0) | (Casting.active==True)).all()

    elif target_county.kingdom in current_user.county.kingdom.enemies:
    targets = 'hostile'
    """

    cls.active_enemy_spells = db.relationship(
        'Casting',
        primaryjoin=(
            "and_("
                "County.id==casting.c.target_id, "
                f"{active_condition}, "
                "casting.c.target_relation=='hostile'"
            ")"
        )

    )

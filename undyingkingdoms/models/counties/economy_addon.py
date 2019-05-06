from sqlalchemy.ext.hybrid import hybrid_property

from ..bases import db


def economy_addon(county_cls, economy_cls):
    """Link Economy and County classes.

    Among other things replicate:
    class County:
        @property
        def produced_grain(self):
            return self.economy.produced_grain

        @produced_grain.setter
        def produced_grain(self, value):
            self.economy.produced_grain = value

    """
    # hoist all columns from economy into county
    cols_to_hoist = set([c.name for c in economy_cls.__table__.c]) - set([c.name for c in county_cls.__table__.c])
    for col in cols_to_hoist:
        prop = hybrid_property(lambda self: getattr(getattr(self, economy_cls.__table__.name), col))
        setattr(
            county_cls,
            col,
            prop
        )
        setattr(
            county_cls,
            col,
            prop.setter(lambda self, value: setattr(getattr(self, economy_cls.__table__.name), col, value))
        )

    # add relationships linking county and economy
    economy_cls.county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    economy_cls. county = db.relationship(
        "County",
        backref=db.backref('economy', uselist=False)
    )

    # add economy object to county init
    orig_init = county_cls.__init__
    # Make copy of original __init__, so we can call it without recursion

    def __init__(self, *args, **kws):
        orig_init(self, *args, **kws)  # Call the original __init__
        self.economy = economy_cls(self)

    county_cls.__init__ = __init__  # Set the class' __init__ to the new one

from sqlalchemy.ext.hybrid import hybrid_property

from utilities.helpers import strip_leading_underscore
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
    cols_to_hoist = set([
        strip_leading_underscore(c.name)
        for c in economy_cls.__table__.c
    ]) - set([
        strip_leading_underscore(c.name)
        for c in county_cls.__table__.c
    ])

    """
    @hybrid_property
    def {col}(self):
        return self.{sub_table}.{col}

    f = hybrid_property(
        lambda self: getattr(getattr(self, 'economy'), 'grain_produced'))
    setattr(County, 'grain_produced', f)
    """
    sub_table = economy_cls.__table__.name
    for name in cols_to_hoist:
        # (lambda name=name: name)()
        # closure problem? name seem take value from calling scope?
        func = hybrid_property(
            lambda self: getattr(
                getattr(self, sub_table),
                name
            )
        )
        setattr(
            county_cls,
            name,  # maybe fix name always being the same?
            func
        )
        setattr(
            county_cls,
            name,
            func.setter(
                lambda self, value: setattr(
                    getattr(self, sub_table),
                    name,
                    value
                )
            )
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

from sqlalchemy.ext.hybrid import hybrid_property

from utilities.helpers import strip_leading_underscore
from ..bases import db


def sub_table_addon(master_cls, slave_cls):
    """Slave a sub table to the master table.

    Example:
        Among other things hoist all columns from economy into county.

    class County:
        @property
        def produced_grain(self):
            return self.economy.produced_grain

        @produced_grain.setter
        def produced_grain(self, value):
            self.economy.produced_grain = value

    @hybrid_property
    def {col}(self):
        return self.{sub_table}.{col}

    f = hybrid_property(
        lambda self: getattr(getattr(self, 'economy'), 'grain_produced'))
    setattr(County, 'grain_produced', f)
    """
    master_table_name = master_cls.__table__.name
    sub_table_name = slave_cls.__table__.name

    cols_to_hoist = set([
        strip_leading_underscore(c.name)
        for c in slave_cls.__table__.c
    ]) - set([
        strip_leading_underscore(c.name)
        for c in master_cls.__table__.c
    ])

    for name in cols_to_hoist:
        func = hybrid_property(
            lambda self, name=name: getattr(
                getattr(self, sub_table_name),
                name
            )
        )
        setattr(
            master_cls,
            name,
            func
        )
        setattr(
            master_cls,
            name,
            func.setter(
                lambda self, value, name=name: setattr(
                    getattr(self, sub_table_name),
                    name,
                    value
                )
            )
        )

    # add relationships linking county and slave table
    slave_cls.county_id = db.Column(
        db.Integer,
        db.ForeignKey(f'{master_table_name}.id'),
        nullable=False
    )
    slave_cls.county = db.relationship(
        master_cls.__name__,
        backref=db.backref(sub_table_name, uselist=False)
    )

    # add sub table object to county init
    # Make copy of original __init__, so we can call it without recursion
    orig_init = master_cls.__init__

    def __init__(self, *args, **kws):
        orig_init(self, *args, **kws)  # Call the original __init__
        setattr(self, sub_table_name, slave_cls(self))

    master_cls.__init__ = __init__  # Set the class' __init__ to the new one

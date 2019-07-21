import pytest
from pattern.text import pluralize

from sqlalchemy.ext.declarative import declared_attr, declarative_base

from extensions import flask_db as db
from lib.namers import to_var_name
from lib.relationship_utils import belongs_to, has_many, has_one


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return to_var_name(cls.__name__)  # pluralize?

    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = db.Column(db.Integer, primary_key=True)


def test_one_to_many(ctx):
    base = declarative_base(cls=Base)

    class Building(base):
        belongs_to("Infrastructure")

    class Infrastructure(base):
        has_many("Buildings")

    db.create_all()

    infrastructure = Infrastructure()
    try:
        infrastructure.buildings
    except AttributeError:
        pytest.fail("relationship was not defined.")

    building = Building()
    try:
        building.infrastructure
    except AttributeError:
        pytest.fail('relationship was not defined.')


def test_one_to_one(ctx):
    base = declarative_base(cls=Base)

    class Account(base):
        belongs_to("Supplier")

    class Supplier(base):
        has_one("Account")

    db.create_all()

    account = Account()
    try:
        account.supplier
    except AttributeError:
        pytest.fail("relationship was not defined.")

    supplier = Supplier()
    try:
        supplier.account
    except AttributeError:
        pytest.fail('relationship was not defined.')

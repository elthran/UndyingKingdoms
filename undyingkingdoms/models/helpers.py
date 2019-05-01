import functools
import os
import random

from flask import current_app
from sqlalchemy.exc import DatabaseError

SEED_SIZE = 5


def get_max_random_int():
    random.seed(os.urandom(SEED_SIZE))
    return random.randint(-2147483648, 2147483647)


def cached_random(func):
    @functools.wraps(func)
    def wrapper(that, *args, **kwargs):
        """Wrap an object's method, allowing access to self.

        Wrapped method's self attribute can be accessed through 'that'
        parameter.

        Requires: Object to have a 'seed' parameter.

        Means you can do:

        class Foo:
            @property
            def seed(self):
                return 42

            @cached_random
            def bar(self, prediction=True):
                pass

        and 'that' will refer to Foo's self parameter.
        Foo must have a 'seed' property of some kind.
        """
        # restore cached seed to allow repeatable randoms
        if 'prediction' in kwargs and kwargs['prediction']:
            random.seed(that.seed)
        return func(that, *args, **kwargs)

    # unset random seed, currently unnecessary
    # random.seed(os.urandom(SEED_SIZE))
    return wrapper


def empty_table(db, name):
    """Truncate the passed table.

    This will wipe the table and reset the index counter.
    """
    db.session.commit()  # prevents hangs
    with db.engine.begin() as con:
        try:
            con.execute("SET FOREIGN_KEY_CHECKS=0;")
            con.execute(f"LOCK TABLES `{name}` WRITE;")
            con.execute(f"TRUNCATE TABLE `{name}`;")
            con.execute("UNLOCK TABLES;")
            con.execute("SET FOREIGN_KEY_CHECKS=1;")
        except Exception as ex:
            print(ex, type(ex))


def delete_table(db, name):
    """Truncate the passed table.

    This will wipe the table and reset the index counter.
    """
    db.session.commit()  # prevents hangs
    with db.engine.begin() as con:
        try:
            con.execute("SET FOREIGN_KEY_CHECKS=0;")
            con.execute(f"LOCK TABLES `{name}` WRITE;")
            con.execute(f"DROP TABLE IF EXISTS `{name}`;")
            con.execute("UNLOCK TABLES;")
            con.execute("SET FOREIGN_KEY_CHECKS=1;")
        except Exception as ex:
            print(ex, type(ex))


def drop_then_rebuild_tables(db, tables):
    """Drops and rebuilds a list of tables."""

    try:
        db.session.commit()  # prevents hangs
    except DatabaseError:
        db.session.rollback()
        raise

    with db.engine.begin() as con:
        con.execute("SET FOREIGN_KEY_CHECKS=0;")
        for table in tables:
            con.execute(f"LOCK TABLES `{table}` WRITE;")
            con.execute(f"DROP TABLE IF EXISTS `{table}`;")
            current_app.logger.info(f"Dropping table `{table}`.")

        db.create_all()
        current_app.logger.info("Recreated all tables.")
        con.execute("SET FOREIGN_KEY_CHECKS=1;")
        con.execute("UNLOCK TABLES;")


def get_target_relation(county, target):
    """Return the relationship between two counties.

    This will get more complex over time and should be optimized.
    """
    if county == target:
        target_relation = 'self'
    elif target.kingdom in county.kingdom.allies:
        target_relation = 'friendly'
    else:
        target_relation = 'hostile'

    # elif target_county.kingdom in county.kingdom.enemies:
    #     targets = 'hostile'
    # else:
    #     targets = 'all'
    # (spell.targets == 'self' and target != county) or
    # (spell.targets == 'friendly' and target.kingdom in county.kingdom.enemies) or
    # (spell.targets == 'hostile' and target.kingdom in county.kingdom.allies) or
    # (spell.targets == 'hostile' and target == county)

    return target_relation

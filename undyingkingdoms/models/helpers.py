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
            con.execute("LOCK TABLES `{}` WRITE;".format(name))
            con.execute("TRUNCATE TABLE `{}`;".format(name))
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
            con.execute("LOCK TABLES `{}` WRITE;".format(name))
            con.execute("DROP TABLE IF EXISTS `{}`;".format(name))
            con.execute("UNLOCK TABLES;")
            con.execute("SET FOREIGN_KEY_CHECKS=1;")
        except Exception as ex:
            print(ex, type(ex))


def drop_then_rebuild_tables(db, tables):
    """Drops and rebuilds a list of tables."""

    try:
        db.session.commit() # prevents hangs
    except DatabaseError:
        db.session.rollback()
        raise

    with db.engine.begin() as con:
        con.execute("SET FOREIGN_KEY_CHECKS=0;")
        for table in tables:
            con.execute("LOCK TABLES `{}` WRITE;".format(table))
            con.execute("DROP TABLE IF EXISTS `{}`;".format(table))
            current_app.logger.info("Dropping table `{}`.".format(table))

        db.create_all()
        current_app.logger.info("Recreated all tables.")
        con.execute("SET FOREIGN_KEY_CHECKS=1;")
        con.execute("UNLOCK TABLES;")

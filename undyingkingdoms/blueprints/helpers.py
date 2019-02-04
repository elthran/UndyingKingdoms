from flask import current_app
from sqlalchemy.exc import DatabaseError


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

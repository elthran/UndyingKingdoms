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
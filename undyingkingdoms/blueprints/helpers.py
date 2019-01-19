def empty_table(db, name):
    """Truncate the passed table.

    This will wipe the table and reset the index counter.
    """
    db.session.commit()  # prevents hangs
    with db.engine.begin() as con:
        try:
            con.execute("SET FOREIGN_KEY_CHECKS=0;")
            con.execute("LOCK TABLES `{}` WRITE".format(name))
            con.execute("TRUNCATE TABLE `{}`;".format(name))
            con.execute("UNLOCK TABLES;".format(name))
            con.execute("SET FOREIGN_KEY_CHECKS=1;")
        except Exception as ex:
            print(ex, type(ex))


def delete_table(engine, name):
    """Truncate the passed table.

    This will wipe the table and reset the index counter.
    """
    engine.execute("SET FOREIGN_KEY_CHECKS=0;")
    engine.execute("DROP TABLE IF EXISTS `{}`;".format(name))
    engine.execute("SET FOREIGN_KEY_CHECKS=1;")

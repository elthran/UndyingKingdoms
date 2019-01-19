def empty_table(engine, name):
    """Truncate the passed table.

    This will wipe the table and reset the index counter.
    """
    try:
        engine.execute("SET FOREIGN_KEY_CHECKS=0;")
        engine.execute("TRUNCATE TABLE `{}`;".format(name))
        engine.execute("SET FOREIGN_KEY_CHECKS=1;")
    except Exception as ex:
        print(ex, type(ex))


def delete_table(engine, name):
    """Truncate the passed table.

    This will wipe the table and reset the index counter.
    """
    engine.execute("SET FOREIGN_KEY_CHECKS=0;")
    engine.execute("DROP TABLE IF EXISTS `{}`;".format(name))
    engine.execute("SET FOREIGN_KEY_CHECKS=1;")

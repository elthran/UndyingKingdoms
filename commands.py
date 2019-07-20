import click
from click import pass_context
from flask.cli import AppGroup, with_appcontext, run_command

from extensions import flask_db as db
from flask import current_app

db_cli = AppGroup('db', help='Various database management commands.')


@db_cli.command('init')
def db_init():
    """Initialize the database."""
    db.create_all()
    click.echo("Create all tables.")


@db_cli.command('drop')
def db_drop():
    """Drop the database."""
    db.engine.execute("SET FOREIGN_KEY_CHECKS=0;")
    db.drop_all()
    db.engine.execute("SET FOREIGN_KEY_CHECKS=1;")
    click.echo("Drop all tables.")


@db_cli.command('populate')
def db_populate():
    """Add data to the database."""
    from seeds import build_testing_objects

    # Create the game world
    build_testing_objects()

    db.session.commit()
    click.echo("Rebuilt all meta-data users.")


@db_cli.command('reset')
@pass_context
def db_reset(ctx):
    """Drops then rebuilds the database."""
    from sqlalchemy import create_engine
    from sqlalchemy_utils import database_exists, create_database

    engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)
    db_drop.invoke(ctx)
    db_init.invoke(ctx)
    db_populate.invoke(ctx)
    click.echo("Database recreated!")


# Testing
@click.command(context_settings={"ignore_unknown_options": True})
@click.argument('args', nargs=-1)
def test(args):
    """Runs unit tests.

    This should run the equivalent of
    `pytest tests -v`
    """

    args = ('tests',) if not args else args

    click.echo(f"Arguments passed to pytest were: {args}")
    import pytest
    pytest.main(list(args))


# Aliases
@click.command('reset')
@with_appcontext
@pass_context
def reset(ctx):
    """Alias for 'db reset'."""
    db_reset.invoke(ctx)


@click.command('serve', context_settings={"ignore_unknown_options": True})
@with_appcontext
@click.argument('args', nargs=-1)
def serve(args):
    """Alias for 'flask run'."""
    ctx = run_command.make_context('serve', list(args))
    run_command.invoke(ctx)

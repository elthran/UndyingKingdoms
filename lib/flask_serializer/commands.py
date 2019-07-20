import os

import click
from flask import render_template_string, current_app
from flask.cli import AppGroup

SERIALIZER_TEMPLATE = """
flask_serializer import Serializer


class {{ model }}Serializer(Serializer):
    def __init__(self, obj):
        self.id = obj.id

"""[1:]  # strips initial newline


create_cli = AppGroup('create', help="Create various components from templates.")


@create_cli.command('serializer')
@click.argument('name')
def create_serializer(name):
    """Create serializer for model of the given name.

    Usage:
        flask create serializer notification

    If name starts with a capital it is used as is.
    If it doesn't title case is used.
    """
    if name[0].isupper():
        model_name = name
    else:
        model_name = name.title()

    template = render_template_string(
        SERIALIZER_TEMPLATE,
        model=model_name,
    )

    root_path = os.path.join(current_app.name, 'serializer')

    if not os.path.isdir(root_path):
        os.mkdir(root_path)
        init_path = os.path.join(root_path, '__init__.py')
        with open(init_path):
            pass

    serializer_path = os.path.join(root_path, model_name + '_serializer.py')
    with open(serializer_path) as f:
        f.write(template)

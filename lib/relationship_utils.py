"""
Implement rails ActiveRecord helpers:

    belongs_to
    has_one
    has_many
    has_many :through
    has_one :through
    has_and_belongs_to_many

"""

import inspect

from pattern.text.en import pluralize, singularize

from lib.namers import to_var_name


def rip_context_info(model_name):
    """Extract the context from the calling class.

    This expects the method to be used like:

    from xxx import yyy as db

    class Foo:
        belongs_to("Bar")
    """
    stack = inspect.stack()[2]
    frame = stack.frame
    db = frame.f_globals['db']
    caller_namespace = frame.f_locals
    calling_class_name = stack.function
    calling_class_table_name = to_var_name(calling_class_name)
    table_name = to_var_name(model_name)

    return caller_namespace, db, table_name, calling_class_table_name


def belongs_to(model_name, nullable=True, unique=False, **fk_kwargs):
    """Generate a one to many relationship."""

    caller_namespace, db, table_name, calling_class_table_name = rip_context_info(model_name)
    variable_name = table_name

    caller_namespace[f'{variable_name}_id'] = db.Column(
        db.Integer,
        db.ForeignKey(f'{table_name}.id', **fk_kwargs),
        nullable=nullable,
        unique=unique,
    )
    plural_name = pluralize(calling_class_table_name)
    caller_namespace[f'{variable_name}'] = db.relationship(
        f'{model_name}',
        back_populates=f'{plural_name}'
    )


def has_one(model_name, **relation_kwargs):
    """Build a one to one relationship."""
    caller_namespace, db, variable_name, calling_class_table_name = rip_context_info(model_name)

    caller_namespace[f'{variable_name}'] = db.relationship(
        f'{model_name}',
        back_populates=f'{calling_class_table_name}',
        uselist=False,
        **relation_kwargs
    )


def has_many(model_name, **relation_kwargs):
    """Build a many to one relationship."""
    singular_model_name = singularize(model_name)
    caller_namespace, db, variable_name, calling_class_table_name = rip_context_info(singular_model_name)
    plural_name = pluralize(variable_name)

    breakpoint()

    caller_namespace[f'{plural_name}'] = db.relationship(
        f'{singular_model_name}',
        back_populates=f'{calling_class_table_name}',
        **relation_kwargs
    )

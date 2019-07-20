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
from lib.namers import to_var_name


def belongs_to(model_name):
    stack = inspect.stack()[1]
    frame = stack.frame
    db = frame.f_globals['db']
    caller_namespace = frame.f_locals
    calling_class_name = stack.function
    calling_class_table_name = to_var_name(calling_class_name)
    table_name = to_var_name(model_name)

    caller_namespace[f'{table_name}_id'] = db.Column(
        db.Integer,
        db.ForeignKey(f'{table_name}.id'),
        nullable=False
    )
    caller_namespace[f'{table_name}'] = db.relationship(
        f'{model_name}',
        back_populates=f'{calling_class_table_name}'
    )


def has_one(model_name):
    stack = inspect.stack()[1]
    frame = stack.frame
    db = frame.f_globals['db']
    caller_namespace = frame.f_locals
    calling_class_name = stack.function
    calling_class_table_name = to_var_name(calling_class_name)
    table_name = to_var_name(model_name)

    caller_namespace[f'{table_name}'] = db.relationship(
        f'{model_name}',
        back_populates=f'{calling_class_table_name}'
    )

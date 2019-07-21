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

from lib.namers import to_var_name, to_class_name

CARDINALITY = 'cardinality'
ONE_TO_MANY = 1
ONE_TO_ONE = 2
global_relations = {}


def rip_context_info(model_name, stack_offset=2, database_name='db'):
    """Extract the context from the calling class.

    This expects the method to be used like:

    from xxx import yyy as db

    class Foo:
        belongs_to("Bar")
    """
    stack = inspect.stack()[stack_offset]
    frame = stack.frame
    db = frame.f_globals[database_name]
    caller_namespace = frame.f_locals
    caller_class_name = stack.function
    caller_table_name = to_var_name(caller_class_name)
    table_name = to_var_name(model_name)

    return caller_namespace, db, table_name, caller_table_name, caller_class_name


def build_relation_callback(
        plural_name, caller_namespace, variable_name, model_name,
        relation_kwargs, db_
):
    """Freeze some args into a callback for building a relation."""

    def relation_callback(
        back_populates=plural_name, namespace=caller_namespace,
        name=variable_name, model=model_name, relation_options=relation_kwargs,
        db=db_
    ):
        """Build allow building of back population once naming is resolved."""
        if back_populates is not None:
            relation_kwargs['back_populates'] = back_populates

        namespace[f'{name}'] = db.relationship(
            f'{model}',
            **relation_options
        )

    return relation_callback


def belongs_to(model_name, nullable=True, unique=False, fk_kwargs=None, relation_kwargs=None):
    """Connect a children to a parent in a one-to-many relationship.

    class Child:
        parent_id = Column(Integer, ForeignKey('parent.id'))
        parent = relationship("Parent")

    When other side of relations is set it activates
        parent = relationship("Parent", back_populates="children|child")

    with back_populates specified by the other side of the relation.
    """

    fk_kwargs = fk_kwargs or {}
    relation_kwargs = relation_kwargs or {}

    caller_namespace, db, table_name, caller_table_name, caller_class_name = rip_context_info(model_name)
    variable_name = table_name

    caller_namespace[f'{variable_name}_id'] = db.Column(
        db.Integer,
        db.ForeignKey(f'{table_name}.id', **fk_kwargs),
        nullable=nullable,
        unique=unique,
    )

    plural_name = pluralize(caller_table_name)

    relation_callback = build_relation_callback(
        plural_name, caller_namespace, variable_name, model_name,
        relation_kwargs, db
    )

    try:
        callback = global_relations[caller_table_name][table_name]
    except KeyError:
        callback = None

    if callback:
        cardinality = global_relations[caller_table_name][CARDINALITY]
        back_populates = pluralize(table_name) if cardinality == ONE_TO_MANY else table_name
        callback(back_populates)  # need to determine cardinality of relation?
    else:
        relation_callback(back_populates=None)
        global_relations[table_name] = {
            caller_table_name: relation_callback,
            CARDINALITY: ONE_TO_MANY,
        }


def has_one(model_name, **relation_kwargs):
    """Connect a parent table to a child in a one-to-one relation.

    class Parent:
        child = relationship("Child", uselist=False, back_populates="parent")
    """

    caller_namespace, db, table_name, caller_table_name, caller_class_name = rip_context_info(model_name)
    variable_name = table_name

    caller_namespace[f'{variable_name}'] = db.relationship(
        f'{model_name}',
        back_populates=f'{caller_table_name}',
        uselist=False,
        **relation_kwargs,
    )


    try:
        callback = global_relations[caller_table_name][table_name]
    except KeyError:
        callback = None

    if callback:
        back_populates = singularize(table_name)
        callback(back_populates)


def has_many(model_name, **relation_kwargs):
    """Connect children to parent in one-to-many relationship.

    class Parent:
        children = relationship("Child", back_populates="parent")
    """
    singular_model_name = singularize(model_name)
    caller_namespace, db, table_name, caller_table_name, caller_class_name = rip_context_info(singular_model_name)
    plural_variable_name = pluralize(table_name)
    singular_class_name = to_class_name(singular_model_name)

    caller_namespace[f'{plural_variable_name}'] = db.relationship(
        f'{singular_class_name}',
        back_populates=f'{caller_table_name}',
        **relation_kwargs
    )

    try:
        callback = global_relations[caller_table_name][table_name]
    except KeyError:
        callback = None

    if callback:
        callback(plural_variable_name)


# def has_parents(model_name, **relation_kwargs):
#     """Connect a child to parents in many-to-one relation.
#
#     parents = relationship("Parent", back_populates="child")
#     """
#     singular_model_name = singularize(model_name)
#     caller_namespace, db, table_name, calling_class_table_name = rip_context_info(singular_model_name)
#     plural_variable_name = pluralize(table_name)
#     singular_class_name = to_class_name(singular_model_name)
#
#     caller_namespace[f'{plural_variable_name}'] = db.relationship(
#         f'{singular_class_name}',
#         back_populates=f'{calling_class_table_name}',
#         **relation_kwargs
#     )


# def has_many(model_name, **relation_kwargs):
#     """Build a many to one relationship."""
#     singular_model_name = singularize(model_name)
#     caller_namespace, db, variable_name, calling_class_table_name = rip_context_info(singular_model_name)
#     plural_name = pluralize(variable_name)
#
#     caller_namespace[f'{plural_name}'] = db.relationship(
#         f'{singular_model_name}',
#         back_populates=f'{calling_class_table_name}',
#         **relation_kwargs
#     )

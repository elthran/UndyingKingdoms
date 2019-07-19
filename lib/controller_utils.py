from functools import wraps
from importlib import import_module
from pkgutil import iter_modules

from flask import Response, jsonify

from lib.namers import to_class_name, to_mixed_case


def load_module_from_finder(finder, package_name, module_name):
    """Load a module from a given package."""
    return finder.find_module(f'{package_name}.{module_name}').load_module()


def add_all_controllers_in_package_to_namespace(package, namespace):
    """Look for and add all controller to the passed namespace.

    Basically an import * from package, returning InfrastructureController, etc.
    """
    for module_finder, name, ispkg in iter_modules(package.__path__):
        if not ispkg and name.endswith('_controller'):
            cls_name = to_class_name(name)
            module = load_module_from_finder(module_finder, package.__name__, name)
            cls = getattr(module, cls_name)
            namespace[cls_name] = cls


def convert_to_view_function(controller):
    """Convert a method into an actual view function for the routing system.

    Internally generates an instance of the class on the fly so as to
    fill the self parameter.
    """
    module = import_module(controller.__module__)
    cls_name, *_, = controller.__qualname__.split('.')
    cls = getattr(module, cls_name)

    @wraps(controller)
    def as_view(*args, **kwargs):
        result = controller(cls(), *args, **kwargs)
        if isinstance(result[0], Response):
            return result
    return as_view

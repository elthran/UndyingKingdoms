from pkgutil import iter_modules

from lib.namers import to_class_name


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

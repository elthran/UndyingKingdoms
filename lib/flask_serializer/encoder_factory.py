import os
import typing
from importlib import import_module

from flask.json import JSONEncoder

from lib.namers import to_class_name


class MetaJSONEncoder(JSONEncoder):
    serializers = None

    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            pass

        if isinstance(obj, typing.Iterable):
            return list(obj)

        try:
            serializer = self.serializers[obj.__class__.__name__]
        except KeyError:
            serializer = None

        if serializer is not None:
            serialized_obj = serializer(obj)
            return serialized_obj.__json__()


def generate_model_name_for_serializer(cls):
    """Return the model a serializer refers too."""

    # FooSerializer -> "Foo" -> "Serializer is stripped"
    return cls.__name__[:-10]


def meta_json_encoder_factory(root):
    """Generates an encoder that uses all serializers for this app.

    Serializers must be placed in the "serializers" folder.
    Serializer modules must be named foo_model_name_serializer.py
    Serializer classes must be named FooModelNameSerializer.

    NOTE: base_serializer.py is ignored (inefficiently).
    """
    imported_serializers = {}
    serializer_package_path = os.path.join(root, "serializers")
    for name in os.listdir(serializer_package_path):
        if name.endswith("_serializer.py"):
            module_name = name.split('.')[0]
            module_path = '.'.join([root, "serializers", module_name])
            module = import_module(module_path)
            serializer_cls_name = to_class_name(module_name)
            serializer = module.__dict__[serializer_cls_name]
            model_name = generate_model_name_for_serializer(serializer)
            imported_serializers[model_name] = serializer

    assert imported_serializers != {}, "should find at least one"
    MetaJSONEncoder.serializers = imported_serializers
    return MetaJSONEncoder

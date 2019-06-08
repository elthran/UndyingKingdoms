# metadata aggregates file.
# could be in the metadata folder?
import os
from importlib import import_module


all_metadata_imports = {}

for root, dirs, files in os.walk("undyingkingdoms/metadata"):
    for name in files:
        if name.endswith(".py"):
            mod_name = name.split('.')[0]
            mod_path = '.'.join(root.split(os.path.sep) + [mod_name])
            all_metadata_imports[mod_name] = import_module(mod_path)

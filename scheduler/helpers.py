import sys
import os


def hack_import_path(file_name):
    path = os.path.dirname(os.path.realpath(file_name))
    if path not in sys.path:
        sys.path = [path] + sys.path

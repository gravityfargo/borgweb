""" plugins/__init__.py """

import os
import traceback
from importlib import util
from flask.views import View


class WebPlugin():
    plugins = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.plugins.append(cls)


def load_module(path):
    name = os.path.split(path)[-1]
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)

for i in os.listdir(dirpath):
    # ignore if is not a directory or starts with __
    if not os.path.isdir(os.path.join(dirpath, i)) or i.startswith("__"):
        continue

    for j in os.listdir(os.path.join(dirpath, i)):
        # ignore if is not a python file or starts with __
        if not j.endswith(".py") or j.startswith("__"):
            continue

        try:
            load_module(os.path.join(dirpath, i, j))
        except Exception:
            traceback.print_exc()

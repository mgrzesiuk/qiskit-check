from importlib import import_module
from typing import Dict


def _get_class_object_from_class_path(class_path: str) -> type:
    module_path, class_name = class_path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, class_name)


def get_object_from_config(config: Dict[str, any]) -> object:
    class_name = config["class"]
    class_object = _get_class_object_from_class_path(class_name)
    arg_key = "args"
    if arg_key in config:
        arguments = config[arg_key]
        return class_object(**arguments)
    return class_object()

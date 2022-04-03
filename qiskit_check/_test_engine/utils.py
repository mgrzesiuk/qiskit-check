from importlib import import_module
from typing import Dict


def _get_class_object_from_class_path(class_path: str) -> type:
    """
    get a class object from given python class path
    Args:
        class_path: python class path to the object

    Returns: class object from specified python path

    """
    module_path, class_name = class_path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, class_name)


def get_object_from_config(config: Dict[str, any]) -> object:
    """
    parse dictionary config and create an object from it, class path has to be specified with class: and
    arguments have to be specified under args: (with nested objects allowed)
    Args:
        config: dictionary containing configuration, obtained from yaml file

    Returns: created object

    """
    class_key = "class"
    class_name = config[class_key]
    class_object = _get_class_object_from_class_path(class_name)
    arg_key = "args"
    if arg_key in config:
        arguments = config[arg_key]
        parsed_arguments = {}
        for key, value in arguments.items():
            if isinstance(value, dict) and class_key in value:
                parsed_arguments[key] = get_object_from_config(value)
            else:
                parsed_arguments[key] = value
        return class_object(**parsed_arguments)
    return class_object()

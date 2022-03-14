import sys
from importlib import import_module
from typing import Dict

from yaml import safe_load

from qiskit_check._test_engine.config.default_config import DefaultConfig
from qiskit_check._test_engine.config.abstract_config import AbstractConfig
from qiskit_check._test_engine.generator import QubitInputGeneratorFactory
from qiskit_check._test_engine.printers import AbstractPrinter
from qiskit_check._test_engine.test_runner import AbstractTestRunner


class Config(AbstractConfig):
    def __init__(self, config_path: str) -> None:
        self.config = safe_load(open(config_path))
        self.default_config = DefaultConfig()

    def get_test_runner(self) -> AbstractTestRunner:
        test_runner_key = "test_runner"
        if self.config is None or test_runner_key not in self.config:
            return self.default_config.get_test_runner()

        return self.get_object_from_config(self.config[test_runner_key])

    def get_printer(self) -> AbstractPrinter:
        printer_key = "printer"
        if self.config is None or printer_key not in self.config:
            return self.default_config.get_printer()

        return self.get_object_from_config(self.config[printer_key])

    def get_input_generator_factory(self) -> QubitInputGeneratorFactory:
        input_generator_factory_key = "input_generator_factory"
        if self.config is None or input_generator_factory_key not in self.config:
            return self.default_config.get_input_generator_factory()

        return self.get_object_from_config(self.config[input_generator_factory_key])

    @staticmethod
    def get_object_from_config(config: Dict[str, any]) -> object:
        class_name = config["class"]
        class_object = Config._get_class_object_from_class_path(class_name)
        arg_key = "args"
        if arg_key in config:
            arguments = config[arg_key]
            return class_object(**arguments)
        return class_object()

    @staticmethod
    def _get_class_object_from_class_path(class_path: str) -> type:
        module_path, class_name = class_path.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)

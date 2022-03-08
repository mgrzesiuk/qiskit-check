from __future__ import absolute_import

import os
import sys
from importlib.util import spec_from_file_location, module_from_spec
from inspect import isabstract
from typing import Set, Type
from uuid import uuid4

from qiskit_check.property_test.property_test import PropertyTest


class Collector:
    def collect(self, directory: str) -> Set[Type[PropertyTest]]:
        absolute_path = os.path.abspath(directory)
        self._import_all_modules_from_directory(absolute_path)
        return self._get_all_test_classes(PropertyTest)

    def _get_all_test_classes(self, cls: Type[PropertyTest]) -> Set[Type[PropertyTest]]:
        subclasses = set()
        for subclass in cls.__subclasses__():
            if not isabstract(subclass):
                subclasses.add(subclass)
            subclasses.update(self._get_all_test_classes(subclass))
        return subclasses

    @staticmethod
    def _import_all_modules_from_directory(directory: str) -> None:
        for dirname, _, files in os.walk(directory):
            for filename in files:
                module_name, extension = os.path.splitext(filename)
                if extension == '.py':
                    module_path = os.path.join(dirname, filename)
                    Collector._import_file(module_path, Collector.generate_global_name(module_name))

    @staticmethod
    def generate_global_name(module_name: str) -> str:
        return module_name + uuid4().__str__()

    # code by Stefan Scherfke published on https://stackoverflow.com/questions/19009932/import-arbitrary-python-source-file-python-3-3/41595552#41595552
    @staticmethod
    def _import_file(module_path: str, global_name: str) -> None:
        spec = spec_from_file_location(global_name, module_path)
        module = module_from_spec(spec)
        sys.modules[global_name] = module
        spec.loader.exec_module(module)

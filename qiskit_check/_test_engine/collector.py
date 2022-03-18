from __future__ import absolute_import

import os
import sys
from importlib.util import spec_from_file_location, module_from_spec
from inspect import isabstract
from pathlib import Path
from typing import Set, Type, Tuple
from uuid import uuid4

from qiskit_check.property_test.property_test import PropertyTest


class Collector:
    def collect(self, path: str) -> Set[Type[PropertyTest]]:
        self._import_all_modules_from_directory(path)
        test_classes, _ = self._get_all_test_classes(PropertyTest, set())
        return test_classes

    def _get_all_test_classes(self, cls: Type[PropertyTest], seen: Set[str]) -> Tuple[Set[Type[PropertyTest]], Set[str]]:
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclass_name = subclass.__name__
            if not isabstract(subclass) and subclass_name not in seen:
                subclasses.add(subclass)
                seen.add(subclass_name)

            collected_subclasses, seen_subclasses = self._get_all_test_classes(subclass, seen)
            subclasses.update(collected_subclasses)
            seen.update(seen_subclasses)

        return subclasses, seen

    @staticmethod
    def _import_all_modules_from_directory(path: str) -> None:
        if os.path.isfile(path):
            module_name = Path(path).name
            Collector._import_file(path, Collector._get_global_name(module_name))
        elif os.path.isdir(path):
            for dirname, _, files in os.walk(path):
                for filename in files:
                    module_name, extension = os.path.splitext(filename)
                    if extension == '.py':
                        module_path = os.path.join(dirname, filename)
                        Collector._import_file(module_path, Collector._get_global_name(module_name))
        else:
            raise ValueError(f"{path} is not a valid path to directory or file")

    @staticmethod
    def _get_global_name(module_name: str) -> str:
        return module_name + uuid4().__str__()

    # code by Stefan Scherfke published on https://stackoverflow.com/questions/19009932/import-arbitrary-python-source-file-python-3-3/41595552#41595552
    @staticmethod
    def _import_file(module_path: str, global_name: str) -> None:
        spec = spec_from_file_location(global_name, module_path)
        module = module_from_spec(spec)
        sys.modules[global_name] = module
        spec.loader.exec_module(module)

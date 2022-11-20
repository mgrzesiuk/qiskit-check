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
    """
    class for collecting property test classes
    """
    def collect(self, path: str) -> Set[Type[PropertyTest]]:
        """
        collect property test classes that inherit from PropertyTest class
        from given destination, property tests must be uniquely named (even if in different files)
        Args:
            path: path to file or directory where/under which property tests are located

        Returns: set of property test class objects found from given destination

        """
        self._import_all_modules_from_directory(path)
        test_classes, _ = self._get_all_test_classes(PropertyTest, set())
        return test_classes

    def _get_all_test_classes(self, cls: Type[PropertyTest], seen: Set[str]) -> Tuple[Set[Type[PropertyTest]], Set[str]]:
        """
        return all test classes that inherit from cls
        Args:
            cls: class of subtype PropertyTest (or PropertyTest class) which subclasses to collect
            seen: set of seen names of the test classes, for recurrence

        Returns: set of property test classes and a set of seen test class names

        """
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
        """
        import all modules from directory or file
        Args:
            path: path to directory or file from which to collect test modules

        Returns: None

        """
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
        """
        generate a unique name for a module (module name + uuid)
        Args:
            module_name: name of the module for which to generate the name

        Returns: unique name for the module

        """
        return module_name + uuid4().__str__()

    @staticmethod
    def _import_file(module_path: str, global_name: str) -> None:
        """
        import file at a module_path and set its global name name to global_name

        code by Stefan Scherfke published on
        https://stackoverflow.com/questions/19009932/import-arbitrary-python-source-file-python-3-3/41595552#41595552
        Args:
            module_path: path to the module to import
            global_name: globala_name for the module

        Returns: None

        """
        spec = spec_from_file_location(global_name, module_path)
        module = module_from_spec(spec)
        sys.modules[global_name] = module
        spec.loader.exec_module(module)

from __future__ import absolute_import

from inspect import isabstract
from importlib import import_module
import os
import sys
from typing import Set, Type

from case_studies.teleportation.tst import TeleportationProperty
from qiskit_check.property_test.property_test import PropertyTest


class Collector:
    def collect(self, directory: str) -> Set[Type[PropertyTest]]:
        absolute_path = self._get_absolute_path(directory)
        self._import_all_modules_from_directory(absolute_path)
        return {TeleportationProperty}
        return self._get_all_test_classes(PropertyTest)

    def _get_all_test_classes(self, cls: Type[PropertyTest]) -> Set[Type[PropertyTest]]:
        subclasses = set()
        for subclass in cls.__subclasses__():
            if not isabstract(subclass):
                subclasses.add(subclass)
            subclasses.update(self._get_all_test_classes(subclass))
        return subclasses

    @staticmethod
    def _get_absolute_path(directory: str) -> str:
        if os.path.isabs(directory):
            return directory
        else:
            return os.path.join(sys.argv[0], directory)

    @staticmethod
    def _import_all_modules_from_directory(directory: str) -> None:
        for dirname, _, files in os.walk(directory):
            for filename in files:
                module_name, extension = os.path.splitext(filename)
                if extension == '.py':
                    Collector._import_file(dirname, module_name, directory)

    @staticmethod
    def _import_file(dirname: str, module_name: str, directory: str) -> None:
        # TODO: does this work with different funky paths? ones which arent also roots - probably not
        # get the top level directory for which modules to import - the root file
        current_root = directory.split(os.path.sep)[-1]
        # remove "absolute" part of the path and leave relative
        relative_path = dirname.replace(directory, '')
        # python modules need to start from the root file
        relative_path = current_root + relative_path
        # join relative path and module name and change separator to . which is accepted as python module separator
        module_path = os.path.join(relative_path, module_name).replace(os.path.sep, '.')
        # import modules
        module = import_module(module_path)
        globals()[module_path] = module
        sys.modules[module_path] = module

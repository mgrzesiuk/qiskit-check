from inspect import isabstract
from os import walk
from os.path import isabs, join
from sys import argv
from typing import Set, Type

from qiskit_check.property_test.property_test import PropertyTest


class Collector:
    def collect(self, directory: str) -> Set[Type[PropertyTest]]:
        absolute_path = self._get_absolute_path(directory)
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
    def _get_absolute_path(directory: str) -> str:
        if isabs(directory):
            return directory
        else:
            return join(argv[0], directory)

    @staticmethod
    def _import_all_modules_from_directory(directory: str) -> None:
        for dirname, _, filename in walk(directory):
            pass



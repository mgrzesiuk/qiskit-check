from typing import List, Type

from qiskit_check.property_test.property_test import PropertyTest


class Collector:
    @staticmethod
    def collect(directory: str) -> List[Type[PropertyTest]]:
        pass

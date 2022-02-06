from typing import List, Type

from qiskit_check.property_test.property_test import PropertyTest


class Collector:
    def collect(self) -> List[Type[PropertyTest]]:
        pass

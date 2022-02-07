from abc import ABC

from qiskit_check.property_test.property_test import PropertyTest


class ExampleTestBase(PropertyTest, ABC):
    @property
    def confidence_level(self) -> float:
        return 0.99

    @property
    def num_test_cases(self) -> int:
        return 1000

    @property
    def num_measurements(self) -> int:
        return 500

    @property
    def num_experiments(self) -> int:
        return 500


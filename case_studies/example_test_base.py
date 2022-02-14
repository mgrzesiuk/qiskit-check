from abc import ABC

from qiskit_check.property_test.property_test import PropertyTest


class ExampleTestBase(PropertyTest, ABC):
    @staticmethod
    def confidence_level() -> float:
        return 0.99

    @staticmethod
    def num_test_cases() -> int:
        return 2

    @staticmethod
    def num_measurements() -> int:
        return 500

    @staticmethod
    def num_experiments() -> int:
        return 500


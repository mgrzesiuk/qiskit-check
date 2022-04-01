from abc import ABC

from qiskit_check.property_test.property_test import PropertyTest


class TestBase(PropertyTest, ABC):
    @staticmethod
    def confidence_level() -> float:
        return 0.99

    @staticmethod
    def num_test_cases() -> int:
        return 10

    @staticmethod
    def num_measurements() -> int:
        return 1024

    @staticmethod
    def num_experiments() -> int:
        return 500


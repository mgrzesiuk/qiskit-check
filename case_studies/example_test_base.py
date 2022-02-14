from abc import ABC#TODO: do 2 of these, one for one by one, other for multithreaded (so just a list at once) (maybe it shouldnt be here and runner should do it - and then it can be one by one genereation)


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


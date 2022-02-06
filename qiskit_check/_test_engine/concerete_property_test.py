from typing import Type

from qiskit_check._test_engine.assessor import AssessorFactory
from qiskit_check._test_engine.generator.input_generator.abstract_input_generator import QubitInputGeneratorFactory
from qiskit_check._test_engine.test_case import TestCaseGenerator, TestCase
from qiskit_check.property_test.property_test import PropertyTest
#TODO: do 2 of these, one for one by one, other for multithreaded (so just a list at once) (maybe it shouldnt be here and runner should do it - and then it can be one by one genereation)


class ConcretePropertyTestIterator:
    def __init__(self, unit_test_generator: TestCaseGenerator, num_test_cases: int) -> None:
        self.unit_test_generator = unit_test_generator
        self.num_test_cases = num_test_cases
        self.num_test_cases_run = 0

    def __next__(self) -> TestCase:
        if self.num_test_cases >= self.num_test_cases_run:
            raise StopIteration()

        self.num_test_cases_run += 1
        return self.unit_test_generator.generate()
 

class ConcretePropertyTest:
    def __init__(
            self, property_test_class: Type[PropertyTest], assessor_factory: AssessorFactory,
            qubit_input_generator_factory: QubitInputGeneratorFactory) -> None:
        self.property_test_class = property_test_class
        self.assessor_factory = assessor_factory
        self.qubit_input_generator_factory = qubit_input_generator_factory

    def __iter__(self) -> ConcretePropertyTestIterator:
        qubit_input_generator = self.qubit_input_generator_factory.build()
        unit_test_generator = TestCaseGenerator(self.property_test_class, self.assessor_factory, qubit_input_generator)
        return ConcretePropertyTestIterator(unit_test_generator, self.property_test_class.num_test_cases())

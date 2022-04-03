from typing import Type

from qiskit_check._test_engine.assessor import AssessorFactory
from qiskit_check._test_engine.generator.abstract_input_generator import QubitInputGeneratorFactory
from qiskit_check._test_engine.concrete_property_test.test_case import TestCaseGenerator, TestCase
from qiskit_check.property_test.property_test import PropertyTest


class ConcretePropertyTestIterator:
    """
    iterator for concrete property test cases
    """
    def __init__(self, unit_test_generator: TestCaseGenerator, max_num_test_cases: int) -> None:
        """
        initialize
        Args:
            unit_test_generator: test case generator
            max_num_test_cases:
        """
        self.unit_test_generator = unit_test_generator
        self.max_num_test_cases = max_num_test_cases
        self.num_test_cases_run = 0

    def __next__(self) -> TestCase:
        """
        return next generated test case for this property test
        Returns: TestCase object, stops iteration once generated all test cases (specified in implementations of
        PropertyTest class by user)

        """
        if self.max_num_test_cases <= self.num_test_cases_run:
            raise StopIteration()

        self.num_test_cases_run += 1
        return self.unit_test_generator.generate()
 

class ConcretePropertyTest:
    """
    this class serves as a template for creation test cases for the given property test class
    """
    def __init__(
            self, property_test_class: Type[PropertyTest], assessor_factory: AssessorFactory,
            qubit_input_generator_factory: QubitInputGeneratorFactory) -> None:
        """
        initialize
        Args:
            property_test_class: property test class object for which the template is made
            assessor_factory: factory object to create assessor objects
            qubit_input_generator_factory: factory object to create qubit input
            generators for generating initial states for tests
        """
        self.property_test_class = property_test_class
        self.assessor_factory = assessor_factory
        self.qubit_input_generator_factory = qubit_input_generator_factory

    def __iter__(self) -> ConcretePropertyTestIterator:
        """
        get iterator that will generate the test cases for this property test
        Returns: iterator

        """
        qubit_input_generator = self.qubit_input_generator_factory.build()
        unit_test_generator = TestCaseGenerator(self.property_test_class, self.assessor_factory, qubit_input_generator)
        return ConcretePropertyTestIterator(unit_test_generator, self.property_test_class.num_test_cases())

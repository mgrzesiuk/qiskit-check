from typing import Tuple, Set, Type, List

from qiskit_check.test_engine.assessor import AssessorFactory
from qiskit_check.test_engine.concrete_property_test.concrete_property_test import ConcretePropertyTest
from qiskit_check.test_engine.generator.abstract_input_generator import QubitInputGeneratorFactory
from qiskit_check.test_engine.test_runner.abstract_test_runner import AbstractTestRunner
from qiskit_check.property_test.property_test import PropertyTest


class Processor:
    def __init__(
            self, assessor_factory: AssessorFactory, qubit_input_generator_factory: QubitInputGeneratorFactory,
            test_runner: AbstractTestRunner) -> None:
        self.assessor_factory = assessor_factory
        self.qubit_input_generator_factory = qubit_input_generator_factory
        self.test_runner = test_runner
        self.printer = self.test_runner.printer

    def process(self, properties_to_test: Set[Type[PropertyTest]]) -> Tuple[List[str], List[str]]:
        self.printer.print_introduction(properties_to_test)
        concrete_property_tests = self._generate_concrete_tests(properties_to_test)
        tests_failed, tests_succeeded = self.test_runner.run_tests(concrete_property_tests)
        self.printer.print_summary(tests_failed, tests_succeeded)
        return tests_succeeded, tests_failed # TODO: some better output here that tells where it went wrong

    def _generate_concrete_tests(self, property_test_classes: Set[Type[PropertyTest]]) -> List[ConcretePropertyTest]:
        concrete_property_tests = []
        for property_test_class in property_test_classes:
            concrete_property_test = ConcretePropertyTest(property_test_class, self.assessor_factory,
                                                          self.qubit_input_generator_factory)
            concrete_property_tests.append(concrete_property_test)
        return concrete_property_tests

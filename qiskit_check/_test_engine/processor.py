from typing import List, Type

from qiskit_check._test_engine.assessor import AssessorFactory
from qiskit_check._test_engine.collector import Collector
from qiskit_check._test_engine.concerete_property_test import ConcretePropertyTest
from qiskit_check._test_engine.generator.input_generator.abstract_input_generator import QubitInputGeneratorFactory
from qiskit_check._test_engine.test_runner.abstract_test_runner import AbstractTestRunner
from qiskit_check.property_test.property_test import PropertyTest


class Processor:
    def __init__(
            self, test_collector: Collector, assessor_factory: AssessorFactory,
            qubit_input_generator_factory: QubitInputGeneratorFactory,
            test_runner: AbstractTestRunner, force_test_run: bool = False) -> None:
        self.test_collector = test_collector
        self.assessor_factory = assessor_factory
        self.qubit_input_generator_factory = qubit_input_generator_factory
        self.test_runner = test_runner
        self.force_test_run = force_test_run

    def process(self) -> None:
        property_test_classes = self.test_collector.collect()
        concrete_property_tests = self._generate_concrete_tests(property_test_classes)
        self.test_runner.run_tests(concrete_property_tests, self.force_test_run)

    def _generate_concrete_tests(self, property_test_classes: List[Type[PropertyTest]]) -> List[ConcretePropertyTest]:
        concrete_property_tests = []
        for property_test_class in property_test_classes:
            concrete_property_test = ConcretePropertyTest(property_test_class,
                                                          self.assessor_factory, self.qubit_input_generator_factory)
            concrete_property_tests.append(concrete_property_test)
        return concrete_property_tests

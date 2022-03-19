from typing import Dict, Sequence, Union

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.property_test import PropertyTest
from qiskit_check.property_test.property_test_errors import IncorrectAssertionError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class Assessor:
    def __init__(
            self, assertions: Union[AbstractAssertion, Sequence[AbstractAssertion]],
            confidence_level: float, resource_matcher: Dict[Qubit, ConcreteQubit]) -> None:
        self.assertions = assertions
        self.resource_matcher = resource_matcher
        self.confidence_level = confidence_level

    def assess(self, experiment_results: TestResult) -> None:
        for assertion in self.assertions:
            p_value = assertion.get_p_value(experiment_results, self.resource_matcher)
            assertion.verify(self.confidence_level, p_value)


class AssessorFactory:
    @staticmethod
    def build(property_test: PropertyTest, resource_matcher: Dict[Qubit, ConcreteQubit]) -> Assessor:
        test_assertions = property_test.assertions(property_test.qubits)
        if isinstance(test_assertions, Sequence):
            for assertion in test_assertions:
                if not isinstance(assertion, AbstractAssertion):
                    raise IncorrectAssertionError(property_test)
            assertions = test_assertions
        elif isinstance(test_assertions, AbstractAssertion):
            assertions = (test_assertions, )
        else:
            raise IncorrectAssertionError(property_test)

        return Assessor(assertions, property_test.confidence_level(), resource_matcher)

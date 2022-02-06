from typing import Dict, List, Sequence, Union

from qiskit_check.property_test.assertion import AbstractAssertion
from qiskit_check.property_test.property_test import PropertyTest
from qiskit_check.property_test.property_test_errors import IncorrectAssertionError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit


class Assessor:
    def __init__(
            self, assertions: Union[AbstractAssertion, Sequence[AbstractAssertion]],
            confidence_level: float, resource_matcher: Dict[Qubit, ConcreteQubit]) -> None:
        self.assertions = assertions
        self.resource_matcher = resource_matcher
        self.confidence_level = confidence_level

    def assess(self, experiment_results: List[Dict[str, int]]) -> None:
        for assertion in self.assertions:
            p_value = assertion.verify(experiment_results, self.resource_matcher)
            if 1 - self.confidence_level > p_value:
                raise AssertionError(f"{assertion.__class__.__name__} failed, p value of the test was {p_value} which "
                                     f"was lower then required {1-self.confidence_level}")


class AssessorFactory:
    @staticmethod
    def build(property_test: PropertyTest, resource_matcher: Dict[Qubit, ConcreteQubit]) -> Assessor:
        if isinstance(property_test.assertions, Sequence):
            for assertion in property_test.assertions:
                if not isinstance(assertion, AbstractAssertion):
                    raise IncorrectAssertionError(property_test)
            assertions = property_test.assertions
        elif isinstance(property_test.assertions, AbstractAssertion):
            assertions = (property_test.assertions, )
        else:
            raise IncorrectAssertionError(property_test)

        return Assessor(assertions, property_test.confidence_level, resource_matcher)

from typing import Dict, Sequence

from qiskit_check._test_engine.p_value_correction import AbstractCorrection
from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.property_test import PropertyTest
from qiskit_check.property_test.property_test_errors import IncorrectAssertionError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult
from qiskit_check._test_engine.state_estimation.tomography_requirement import TomographyRequirement


class Assessor:
    def __init__(
            self, assertions: Sequence[AbstractAssertion], confidence_level: float,
            resource_matcher: Dict[Qubit, ConcreteQubit], tomography_requirement: TomographyRequirement) -> None:
        self.assertions = assertions
        self.resource_matcher = resource_matcher
        self.confidence_level = confidence_level
        self.tomography_requirement = tomography_requirement

    def assess(self, experiment_results: TestResult, corrector: AbstractCorrection) -> None:
        for assertion in self.assertions:
            p_value = assertion.get_p_value(experiment_results, self.resource_matcher)
            confidence_level = corrector.get_corrected_confidence_leven()
            assertion.verify(confidence_level, p_value)


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

        tomography_requirement = TomographyRequirement(assertions)

        return Assessor(assertions, property_test.confidence_level(), resource_matcher, tomography_requirement)

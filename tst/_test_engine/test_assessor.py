from typing import Dict, Sequence, Union

import pytest
from pytest_mock import MockFixture
from qiskit import QuantumCircuit

from qiskit_check._test_engine.assessor import Assessor, AssessorFactory
from qiskit_check._test_engine.p_value_correction import AbstractCorrection
from qiskit_check.property_test import PropertyTest
from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.property_test_errors import IncorrectAssertionError
from qiskit_check.property_test.resources import Qubit, ConcreteQubit
from qiskit_check.property_test.test_results import TestResult


class NotAssertion:
    pass


class ExampleAssertion(AbstractAssertion):
    def get_p_value(self, experiments: TestResult, resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        return 1


class ExamplePropertyTest(PropertyTest):
    def __init__(self, assertions):
        super().__init__()
        self.assertions_storage = assertions

    @property
    def circuit(self) -> QuantumCircuit:
        return None

    def get_qubits(self) -> Sequence[Qubit]:
        return []

    def assertions(self, qubits: Sequence[Qubit]) -> Union[AbstractAssertion, Sequence[AbstractAssertion]]:
        return self.assertions_storage

    @staticmethod
    def confidence_level() -> float:
        return 1

    @staticmethod
    def num_test_cases() -> int:
        return 1

    @staticmethod
    def num_measurements() -> int:
        return 1

    @staticmethod
    def num_experiments() -> int:
        return 1


class TestAssessor:
    def test_assess_assertion_error_when_assertion_fails(self, mocker: MockFixture):
        assertion1_mock = mocker.patch("qiskit_check.property_test.assertions.AbstractAssertion", spec=True)
        assertion1_mock.verify.side_effect = AssertionError()
        assertion1_mock.get_p_value.return_value = 0.001

        conf_level = 0.99
        experiment_results = mocker.MagicMock()
        resource_matcher = mocker.MagicMock()
        corrector = mocker.patch.object(AbstractCorrection, "get_corrected_confidence_level")
        corrector.get_corrected_confidence_level.return_value = mocker.MagicMock()

        assessor = Assessor([assertion1_mock], conf_level, resource_matcher, mocker.MagicMock)
        with pytest.raises(AssertionError):
            assessor.assess(experiment_results, corrector, 5, 5)

        assertion1_mock.get_p_value.assert_called_once_with(experiment_results, resource_matcher, 5, 5)
        assertion1_mock.verify.assert_called_once_with(
            corrector.get_corrected_confidence_level.return_value, assertion1_mock.get_p_value.return_value)
        corrector.get_corrected_confidence_level.assert_called_once()

    def test_assess_nothing_happens_when_assertion_pass(self, mocker: MockFixture):
        assertion1_mock = mocker.patch("qiskit_check.property_test.assertions.AbstractAssertion", spec=True)
        assertion1_mock.get_p_value.return_value = 0.001

        conf_level = 0.99
        experiment_results = mocker.MagicMock()
        resource_matcher = mocker.MagicMock()
        corrector = mocker.patch.object(AbstractCorrection, "get_corrected_confidence_level")
        corrector.get_corrected_confidence_level.return_value = mocker.MagicMock()

        assessor = Assessor([assertion1_mock], conf_level, resource_matcher, mocker.MagicMock)
        assessor.assess(experiment_results, corrector, 123, 34512)

        assertion1_mock.get_p_value.assert_called_once_with(experiment_results, resource_matcher, 123, 34512)
        assertion1_mock.verify.assert_called_once_with(
            corrector.get_corrected_confidence_level.return_value, assertion1_mock.get_p_value.return_value)
        corrector.get_corrected_confidence_level.assert_called_once()

    def test_assess_assertion_error_when_multiple_assertions_fail(self, mocker: MockFixture):
        assertion1_mock = mocker.patch("qiskit_check.property_test.assertions.AbstractAssertion", spec=True)
        assertion1_mock.get_p_value.return_value = 0.001

        assertion2_mock = mocker.patch("qiskit_check.property_test.assertions.AbstractAssertion", spec=True)
        assertion2_mock.verify.side_effect = AssertionError()
        assertion2_mock.get_p_value.return_value = 0.0011

        conf_level = 0.99
        experiment_results = mocker.MagicMock()
        resource_matcher = mocker.MagicMock()
        corrector = mocker.patch.object(AbstractCorrection, "get_corrected_confidence_level")
        corrector.get_corrected_confidence_level.return_value = mocker.MagicMock()

        assessor = Assessor([assertion1_mock, assertion2_mock], conf_level, resource_matcher, mocker.MagicMock)
        with pytest.raises(AssertionError):
            assessor.assess(experiment_results, corrector, 123, 5324)

        assertion1_mock.get_p_value.assert_called_once_with(experiment_results, resource_matcher, 123, 5324)
        assertion1_mock.verify.assert_called_once_with(
            corrector.get_corrected_confidence_level.return_value, assertion1_mock.get_p_value.return_value)
        assertion2_mock.get_p_value.assert_called_once_with(experiment_results, resource_matcher)
        assertion2_mock.verify.assert_called_once_with(
            corrector.get_corrected_confidence_level.return_value, assertion2_mock.get_p_value.return_value)
        corrector.get_corrected_confidence_level.assert_called()

    def test_assess_nothing_happens_when_multiple_assertions_pass(self, mocker: MockFixture):
        assertion1_mock = mocker.patch("qiskit_check.property_test.assertions.AbstractAssertion", spec=True)
        assertion1_mock.get_p_value.return_value = 0.001

        assertion2_mock = mocker.patch("qiskit_check.property_test.assertions.AbstractAssertion", spec=True)
        assertion2_mock.get_p_value.return_value = 0.0011

        conf_level = 0.99
        experiment_results = mocker.MagicMock()
        resource_matcher = mocker.MagicMock()
        corrector = mocker.patch.object(AbstractCorrection, "get_corrected_confidence_level")
        corrector.get_corrected_confidence_level.return_value = mocker.MagicMock()

        assessor = Assessor([assertion1_mock, assertion2_mock], conf_level, resource_matcher, mocker.MagicMock)
        assessor.assess(experiment_results, corrector, 312, 321)

        assertion1_mock.get_p_value.assert_called_once_with(experiment_results, resource_matcher, 312, 321)
        assertion1_mock.verify.assert_called_once_with(
            corrector.get_corrected_confidence_level.return_value, assertion1_mock.get_p_value.return_value)
        assertion2_mock.get_p_value.assert_called_once_with(experiment_results, resource_matcher, 312, 321)
        assertion2_mock.verify.assert_called_once_with(
            corrector.get_corrected_confidence_level.return_value, assertion2_mock.get_p_value.return_value)
        corrector.get_corrected_confidence_level.assert_called()

    def test_build_correct_result_when_list_of_assertions_provided(self, mocker: MockFixture):
        property_test = ExamplePropertyTest([ExampleAssertion(), ExampleAssertion()])
        resource_matcher = mocker.MagicMock()
        assessor_factory = AssessorFactory()
        assert isinstance(assessor_factory.build(property_test, resource_matcher), Assessor)

    def test_build_correct_result_when_single_assertion_provided(self, mocker: MockFixture):
        property_test = ExamplePropertyTest(ExampleAssertion())
        resource_matcher = mocker.MagicMock()
        assessor_factory = AssessorFactory()
        assert isinstance(assessor_factory.build(property_test, resource_matcher), Assessor)

    def test_build_raises_incorrect_assertion_when_list_of_not_assertion_provided(self, mocker: MockFixture):
        property_test = ExamplePropertyTest([ExampleAssertion(), NotAssertion()])
        resource_matcher = mocker.MagicMock()
        assessor_factory = AssessorFactory()
        with pytest.raises(IncorrectAssertionError):
            assessor_factory.build(property_test, resource_matcher)

    def test_build_raises_incorrect_assertion_when_not_assertion_provided(self, mocker: MockFixture):
        property_test = ExamplePropertyTest(NotAssertion())
        resource_matcher = mocker.MagicMock()
        assessor_factory = AssessorFactory()
        with pytest.raises(IncorrectAssertionError):
            assessor_factory.build(property_test, resource_matcher)

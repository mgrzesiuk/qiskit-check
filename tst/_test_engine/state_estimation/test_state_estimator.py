import pytest
from pytest_mock import MockFixture

from qiskit_check._test_engine.assessor import Assessor
from qiskit_check._test_engine.concrete_property_test.test_case import TestCase
from qiskit_check._test_engine.state_estimation.state_estimator import StateEstimator
from qiskit_check._test_engine.state_estimation.tomography import AbstractTomography
from qiskit_check._test_engine.state_estimation.tomography_requirement import TomographyRequirement
from qiskit_check.property_test.property_test_errors import NoTomographyError


class TestStateEstimator:
    def test_run_no_tomography_error_when_requires_tomography_but_no_specified(self, mocker: MockFixture):
        state_estimator = StateEstimator(None)
        assessor = mocker.patch.object(Assessor, "assess")
        tomography_requirement = mocker.patch.object(TomographyRequirement, "_parse_assertions")
        requires_tomography = mocker.MagicMock()
        requires_tomography.return_value = True
        tomography_requirement.attach_mock(requires_tomography, "requires_tomography")
        assessor.attach_mock(tomography_requirement, "tomography_requirement")
        qc = mocker.MagicMock()
        test_case = TestCase(assessor, qc, 2, 4)
        run_circuit = mocker.MagicMock()
        with pytest.raises(NoTomographyError):
            state_estimator.run(test_case, run_circuit)

        run_circuit.assert_not_called()

    def test_run_returns_none_when_no_required_tomography_and_none_specified(self, mocker: MockFixture):
        state_estimator = StateEstimator(None)
        assessor = mocker.PropertyMock()
        tomography_requirement = mocker.PropertyMock()
        tomography_requirement.requires_tomography = False
        assessor.tomography_requirement = tomography_requirement
        qc = mocker.MagicMock()
        test_case = TestCase(qc, assessor, 2, 4)
        run_circuit = mocker.MagicMock()

        assert state_estimator.run(test_case, run_circuit) is None
        run_circuit.assert_not_called()

    def test_run_returns_none_when_no_required_tomography_and_specified(self, mocker: MockFixture):
        tomography = mocker.patch.object(AbstractTomography, "estimate_state")
        state_estimator = StateEstimator(tomography)
        assessor = mocker.PropertyMock()
        tomography_requirement = mocker.PropertyMock()
        tomography_requirement.requires_tomography = False
        assessor.tomography_requirement = tomography_requirement
        qc = mocker.MagicMock()
        test_case = TestCase(qc, assessor, 2, 4)
        run_circuit = mocker.MagicMock()

        assert state_estimator.run(test_case, run_circuit) is None
        run_circuit.assert_not_called()

from math import pi

import pytest
from pytest_mock import MockFixture
from qiskit.quantum_info import Statevector
from scipy.spatial.transform import Rotation

from qiskit_check.property_test.assertions import AssertTeleportedByProbability
from qiskit_check.property_test.property_test_errors import NoExperimentsError
from qiskit_check.property_test.resources import Qubit, AnyRange, ConcreteQubit


class TestAssertTransformed:
    def test_check_if_experiments_empty_throws_no_experiments_error_when_no_experiments(self):
        q0 = Qubit(AnyRange())

        assert_transformed = AssertTeleportedByProbability(q0, Rotation.identity())
        test_results = TestResult([], 1000, None)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }

        with pytest.raises(NoExperimentsError):
            assert_transformed.get_p_value(test_results, resource_matcher)

    def test_get_p_value_returns_0_when_not_transformed(self, mocker: MockFixture):
        q0 = Qubit(AnyRange())
        measurement_result = mocker.patch.object(MeasurementResult, "get_qubit_result")

        def get_result(qubit, state):
            if state == "0":
                return 1000
            elif state == "1":
                return 0

        measurement_result.get_qubit_result.side_effect = get_result
        measurement_results = [measurement_result for _ in range(1000)]
        test_results = TestResult(measurement_results, 1000, None)
        assert_transformed = AssertTeleportedByProbability(q0, Rotation.from_euler("X", [pi]))
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert 0 == assert_transformed.get_p_value(test_results, resource_matcher)

    def test_get_p_value_returns_1_when_correctly_transformed(self, mocker: MockFixture):
        q0 = Qubit(AnyRange())
        measurement_result = mocker.patch.object(MeasurementResult, "get_qubit_result")

        def get_result(qubit, state):
            if state == "0":
                return 0
            elif state == "1":
                return 1000

        measurement_result.get_qubit_result.side_effect = get_result
        measurement_results = [measurement_result for _ in range(1000)]
        test_results = TestResult(measurement_results, 1000, None)
        assert_transformed = AssertTeleportedByProbability(q0, Rotation.from_euler("X", [pi]))
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert 0 == assert_transformed.get_p_value(test_results, resource_matcher)

    def test_verify_nothing_happens_when_correct(self):
        q0 = Qubit(AnyRange())
        assert_transformed = AssertTeleportedByProbability(q0, Rotation.identity())
        assert_transformed.verify(0.99, 0.45)

    def test_verify_assertion_error_thrown_when_not_correct(self):
        q0 = Qubit(AnyRange())
        assert_transformed = AssertTeleportedByProbability(q0, Rotation.identity())
        with pytest.raises(AssertionError):
            assert_transformed.verify(0.9, 0.05)

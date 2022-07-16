from math import pi

import pytest
from pytest_mock import MockFixture
from qiskit.quantum_info import Statevector
from scipy.spatial.transform import Rotation

from qiskit_check.property_test.assertions import AssertTransformedByState
from qiskit_check.property_test.resources import AnyRange, Qubit, ConcreteQubit


class TestStateTransformed:
    def test_check_if_experiments_empty_throws_no_tomography_error_when_no_experiments(self):
        q0 = Qubit(AnyRange())
        test_results = TestResult([], 1000, None)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert_transformed = AssertTransformedByState(q0, 0, Rotation.identity())

        with pytest.raises(NoTomographyError):
            assert_transformed.get_p_value(test_results, resource_matcher)

    def test_get_p_value_returns_1_if_transformed(self, mocker: MockFixture):
        q0 = Qubit(AnyRange())
        tomography_result = mocker.patch.object(TomographyResult, "get_estimates")
        tomography_result.get_estimates.return_value = [(0, 0, -1) for _ in range(1000)]
        test_results = TestResult([], 1000, tomography_result)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert_transformed = AssertTransformedByState(q0, 0, Rotation.from_euler("X", [pi]))

        assert 1 == assert_transformed.get_p_value(test_results, resource_matcher)

    def test_get_p_value_returns_0_if_not_transformed(self, mocker: MockFixture):
        q0 = Qubit(AnyRange())
        tomography_result = mocker.patch.object(TomographyResult, "get_estimates")
        tomography_result.get_estimates.return_value = [(0, 0, -1) for _ in range(1000)]
        test_results = TestResult([], 1000, tomography_result)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert_transformed = AssertTransformedByState(q0, 0, Rotation.identity())

        assert 0 == assert_transformed.get_p_value(test_results, resource_matcher)

    def test_verify_throws_assertion_error_when_not_equal(self):
        q0 = Qubit(AnyRange())

        assert_transformed = AssertTransformedByState(q0, 0, Rotation.identity())

        with pytest.raises(AssertionError):
            assert_transformed.verify(0.99, 0.001)

    def test_verify_does_nothing_when_equal(self):
        q0 = Qubit(AnyRange())

        assert_transformed = AssertTransformedByState(q0, 0, Rotation.identity())

        assert_transformed.verify(0.99, 0.1)

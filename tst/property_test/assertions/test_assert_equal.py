from random import randint

import pytest
from pytest_mock import MockFixture
from qiskit.quantum_info import Statevector

from qiskit_check.property_test.assertions import AssertEqual
from qiskit_check.property_test.property_test_errors import NoExperimentsError
from qiskit_check.property_test.resources import Qubit, AnyRange, ConcreteQubit
from qiskit_check.property_test.test_results import MeasurementResult, TestResult


class TestAssertEqual:
    def test_check_if_experiments_empty_throws_no_experiments_error_when_no_experiments(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        assert_entangled = AssertEqual(q0, q1)
        test_results = TestResult([], 1000, None)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }

        with pytest.raises(NoExperimentsError):
            assert_entangled.get_p_value(test_results, resource_matcher)

    def test_get_p_value_returns_0_when_completely_not_equal(self, mocker: MockFixture):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        def get_result(qubit, state):
            if qubit == 0:
                return 1000
            if qubit == 1:
                return 0

        measurement_result = mocker.patch.object(MeasurementResult, "get_qubit_result")
        measurement_result.get_qubit_result.side_effect = get_result
        measurement_results = [measurement_result for _ in range(1000)]
        test_results = TestResult(measurement_results, 1000, None)
        assert_equal = AssertEqual(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 0 == assert_equal.get_p_value(test_results, resource_matcher)

    def test_get_p_value_returns_1_when_completely_equal(self, mocker: MockFixture):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        def get_result(qubit, state):
            if qubit == 0:
                return 1000
            if qubit == 1:
                return 1000

        measurement_result = mocker.patch.object(MeasurementResult, "get_qubit_result")
        measurement_result.get_qubit_result.side_effect = get_result
        measurement_results = [measurement_result for _ in range(1000)]
        test_results = TestResult(measurement_results, 1000, None)
        assert_equal = AssertEqual(q0, q1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
            q1: ConcreteQubit(1, Statevector([1, 0]))
        }
        assert 1 == assert_equal.get_p_value(test_results, resource_matcher)


    def test_verify_throws_assertion_error_when_not_equal(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        assert_entangled = AssertEqual(q0, q1)

        with pytest.raises(AssertionError):
            assert_entangled.verify(0.99, 0.001)

    def test_verify_does_nothing_when_equal(self):
        q0 = Qubit(AnyRange())
        q1 = Qubit(AnyRange())

        assert_entangled = AssertEqual(q0, q1)

        assert_entangled.verify(0.99, 0.1)

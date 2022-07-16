import pytest
from pytest_mock import MockFixture
from qiskit.quantum_info import Statevector

from qiskit_check.property_test.assertions import AssertProbability
from qiskit_check.property_test.property_test_errors import NoExperimentsError
from qiskit_check.property_test.resources import Qubit, AnyRange, ConcreteQubit


class TestAssertProbability:
    def test_check_if_experiments_empty_throws_no_experiments_error_when_no_experiments(self):
        q0 = Qubit(AnyRange())

        assert_probability = AssertProbability(q0, "0", 1)
        test_results = TestResult([], 1000, None)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }

        with pytest.raises(NoExperimentsError):
            assert_probability.get_p_value(test_results, resource_matcher)

    def test_get_p_value_returns_0_when_wrong_probability(self, mocker: MockFixture):
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
        assert_probability = AssertProbability(q0, "1", 1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert 0 == assert_probability.get_p_value(test_results, resource_matcher)

    def test_get_p_value_returns_1_when_correct_probability(self, mocker: MockFixture):
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
        assert_probability = AssertProbability(q0, "0", 1)
        resource_matcher = {
            q0: ConcreteQubit(0, Statevector([1, 0])),
        }
        assert 1 == assert_probability.get_p_value(test_results, resource_matcher)

    def test_verify_nothing_happens_when_correct(self):
        q0 = Qubit(AnyRange())
        assert_probability = AssertProbability(q0, "0", 1)
        assert_probability.verify(0.99, 0.45)

    def test_verify_assertion_error_thrown_when_not_correct(self):
        q0 = Qubit(AnyRange())
        assert_probability = AssertProbability(q0, "0", 1)
        with pytest.raises(AssertionError):
            assert_probability.verify(0.9, 0.05)

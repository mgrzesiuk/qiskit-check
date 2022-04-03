from math import pi, radians

import pytest

from qiskit_check.property_test.resources import QubitRange, AnyRange, DegreeRange


class TestQubitRange:
    def test_qubit_range_input_fixed_when_inverted_input(self):
        theta_start = pi / 2
        theta_end = pi / 3
        phi_start = pi / 3
        phi_end = pi / 4

        qubit_range = QubitRange(theta_start, phi_start, theta_end, phi_end)

        assert qubit_range.phi_end == phi_start
        assert qubit_range.phi_start == phi_end
        assert qubit_range.theta_start == theta_end
        assert qubit_range.theta_end == theta_start

    def test_qubit_range_correct_when_normal_input(self):
        theta_start = pi / 3
        theta_end = pi / 2
        phi_start = pi / 4
        phi_end = pi / 3

        qubit_range = QubitRange(theta_start, phi_start, theta_end, phi_end)

        assert qubit_range.phi_end == phi_end
        assert qubit_range.phi_start == phi_start
        assert qubit_range.theta_start == theta_start
        assert qubit_range.theta_end == theta_end

    def test_qubit_range_value_error_thrown_when_theta_greater_then_pi(self):
        theta_start = pi / 3
        theta_end = pi + 0.2
        phi_start = pi / 4
        phi_end = pi / 3

        with pytest.raises(ValueError):
            QubitRange(theta_start, phi_start, theta_end, phi_end)

    def test_qubit_range_value_error_thrown_when_theta_less_then_0(self):
        theta_start = -0.1
        theta_end = pi
        phi_start = pi / 4
        phi_end = pi / 3

        with pytest.raises(ValueError):
            QubitRange(theta_start, phi_start, theta_end, phi_end)

    def test_qubit_range_value_error_thrown_when_phi_greater_then_2pi(self):
        theta_start = pi / 3
        theta_end = pi / 2
        phi_start = pi / 4
        phi_end = 2*pi + 0.1

        with pytest.raises(ValueError):
            QubitRange(theta_start, phi_start, theta_end, phi_end)

    def test_qubit_range_value_error_thrown_when_phi_less_then_0(self):
        theta_start = pi / 3
        theta_end = pi / 2
        phi_start = -0.2
        phi_end = pi / 3

        with pytest.raises(ValueError):
            QubitRange(theta_start, phi_start, theta_end, phi_end)

    def test_degree_range_input_fixed_when_inverted_input(self):
        theta_start = 90
        theta_end = 60
        phi_start = 60
        phi_end = 45

        qubit_range = DegreeRange(theta_start, phi_start, theta_end, phi_end)

        assert qubit_range.phi_end == radians(phi_start)
        assert qubit_range.phi_start == radians(phi_end)
        assert qubit_range.theta_start == radians(theta_end)
        assert qubit_range.theta_end == radians(theta_start)

    def test_degree_range_correct_when_normal_input(self):
        theta_start = 60
        theta_end = 90
        phi_start = 60
        phi_end = 135

        qubit_range = DegreeRange(theta_start, phi_start, theta_end, phi_end)

        assert qubit_range.phi_end == radians(phi_end)
        assert qubit_range.phi_start == radians(phi_start)
        assert qubit_range.theta_start == radians(theta_start)
        assert qubit_range.theta_end == radians(theta_end)

    def test_degree_range_value_error_thrown_when_theta_greater_then_pi(self):
        with pytest.raises(ValueError):
            DegreeRange(60, 45, 182, 140)

    def test_degree_range_value_error_thrown_when_theta_less_then_0(self):
        with pytest.raises(ValueError):
            DegreeRange(-2, 23, 67, 87)

    def test_degree_range_value_error_thrown_when_phi_greater_then_2pi(self):
        with pytest.raises(ValueError):
            DegreeRange(60, 275, 135, 365)

    def test_degree_range_value_error_thrown_when_phi_less_then_0(self):
        with pytest.raises(ValueError):
            DegreeRange(60, -2, 135, 345)

    def test_any_range_correct_values(self):
        qubit_range = AnyRange()
        assert qubit_range.theta_start == 0
        assert qubit_range.theta_end == pi
        assert qubit_range.phi_start == 0
        assert qubit_range.phi_end == 2 * pi

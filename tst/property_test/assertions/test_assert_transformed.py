from math import pi

from qiskit import QuantumCircuit

from qiskit_check.property_test.assertions import AssertTransformed


class TestAssertTransformed:
    def __init__(self):
        self.assertion = AssertTransformed
        self.angles = [0, pi/4, pi/3, pi/2, 2*pi/3, 3*pi/4, pi, pi + pi/4, pi + pi/3, pi + pi/2, pi + 2*pi/3, pi + 3*pi/4, pi + pi]

    def test_verify_x_gate(self):
        pass

    def test_get_p_value_x_gate(self):
        pass

    def test_verify_h_gate(self):
        pass

    def test_get_p_value_h_gate(self):
        pass

    def test_verify_s_gate(self):
        pass

    def test_get_p_value_s_gate(self):
        pass

    def test_verify_ry_gate(self):
        pass

    def test_get_p_value_ry_gate(self):
        pass

    def test_verify_rx_gate(self):
        pass

    def test_get_p_value_rx_gate(self):
        pass

    def test_verify_rz_gate(self):
        pass

    def test_get_p_value_rz_gate(self):
        pass

    def _get_test_results(self, circuit: QuantumCircuit):
        pass

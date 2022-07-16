from math import pi, sqrt

import pytest

from qiskit_check.property_test.utils import hopf_coordinates_to_bloch_vector
from qiskit_check.property_test.utils import hopf_coordinates_to_vector_state, vector_state_to_hopf_coordinates


class TestUtils:

    def test_hopf_coordinates_to_bloch_vector_correct_vector_with_zero_state(self):
        assert pytest.approx(hopf_coordinates_to_bloch_vector(0, 0)) == (0, 0, 1)

    def test_hopf_coordinates_to_bloch_vector_correct_vector_with_one_state(self):
        assert pytest.approx(hopf_coordinates_to_bloch_vector(pi, 0)) == (0, 0, -1)

    def test_hopf_coordinates_to_vector_state_correct_vector_with_zero_state(self):
        assert pytest.approx(hopf_coordinates_to_vector_state(0, 0)) == (1, 0)

    def test_hopf_coordinates_to_vector_state_correct_vector_with_minus_state(self):
        assert pytest.approx(hopf_coordinates_to_vector_state(pi/2, pi)) == (1/sqrt(2), -1/sqrt(2))

    def test_vector_state_to_hopf_coordinates_correct_coordinates_with_one_state(self):
        assert pytest.approx(vector_state_to_hopf_coordinates(1, 0)) == (0, 0)

    def test_vector_state_to_hopf_coordinates_correct_coordinates_with_plus_state(self):
        assert pytest.approx(vector_state_to_hopf_coordinates(1/sqrt(2), 1/sqrt(2))) == (pi/2, 0)

from cmath import polar, cos, exp, sin, phase
from math import acos
from typing import Tuple


def vector_state_to_hopf_coordinates(
        ground_state_amplitude: complex, excited_state_amplitude: complex) -> Tuple[float, float]:
    """
    :param ground_state_amplitude:
    :param excited_state_amplitude:
    :return:
    """
    ground_state_abs, ground_state_phase = polar(ground_state_amplitude)
    excited_state_phase = phase(excited_state_amplitude)

    theta = 2 * acos(ground_state_abs)
    relative_phase = excited_state_phase - ground_state_phase

    return theta, relative_phase


def hopf_coordinates_to_vector_state(angle: float, relative_phase: float) -> Tuple[complex, complex]:
    ground_state_amp = cos(angle/2)
    excited_state_amp = exp(relative_phase*1j) * sin(angle/2)
    return ground_state_amp, excited_state_amp

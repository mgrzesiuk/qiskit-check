from cmath import polar, cos, exp, sin, phase
from math import acos, sin, pi
from math import cos as fcos
from math import sin as fsin
from typing import Tuple


def vector_state_to_hopf_coordinates(
        ground_state_amplitude: complex, excited_state_amplitude: complex) -> Tuple[float, float]:
    """
    transform vector state of form a|0>+b|1> where a is ground state amplitude and b is excited state amplitude
    into hopf coordinates
    Args:
        ground_state_amplitude: amplitude of zero state (a in a|0> + b|1>)
        excited_state_amplitude: amplitude of one state (b in a|0> + b|1>)

    Returns: hopf coordinates of the input state

    """
    ground_state_abs, ground_state_phase = polar(ground_state_amplitude)
    excited_state_phase = phase(excited_state_amplitude)

    theta = 2 * acos(ground_state_abs)
    relative_phase = excited_state_phase - ground_state_phase

    if relative_phase < 0:
        relative_phase += 2*pi

    return round(theta, 10), round(relative_phase, 10)


def hopf_coordinates_to_vector_state(theta: float, phi: float) -> Tuple[complex, complex]:
    """
    transform hopf coordinates into vector state where a = cos(theta/2) and b = e^(i*phi)*sin(theta/2)
    Args:
        theta: theta coordinate in cos(theta/2) |0> + e^(i*phi)*sin(theta/2) |1> (in radians)
        phi: phi coordinate in cos(theta/2) |0> + e^(i*phi)*sin(theta/2) (in radians)

    Returns: a, b - amplitudes of 0 and 1 respectively

    """
    ground_state_amp = cos(theta/2)
    excited_state_amp = exp(phi*1j) * sin(theta/2)
    return ground_state_amp, excited_state_amp


def hopf_coordinates_to_bloch_vector(theta: float, phi: float) -> Tuple[float, float, float]:
    """
    transform hopf coordinates to 3d vector in cartesian coordinates
    Args:
        theta: theta coordinate in cos(theta/2) |0> + e^(i*phi)*sin(theta/2) |1> (in radians)
        phi: phi coordinate in cos(theta/2) |0> + e^(i*phi)*sin(theta/2) (in radians)

    Returns: 3 d vector, x y z coordinates of the point respectively

    """
    return round_floats(fcos(phi)*fsin(theta)), round_floats(fsin(phi)*fsin(theta)), round_floats(fcos(theta))


def amend_instruction_location(location: int) -> int:
    """
    update circuit instruction location to account for internal circuit modifications
    Args:
        location: initial circuit instruction location

    Returns: real location after accounting for internal circuit modifications

    """
    return location + 1


def round_floats(num):
    return round(num, 10)

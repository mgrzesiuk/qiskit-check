from math import radians, pi


class QubitRange:
    """
    specify possible qubit states with use of hopf coordinates and radians
    """
    def __init__(
            self, theta_start: float, phi_start: float,
            theta_end: float, phi_end: float) -> None:
        """
        initialize
        Args:
            theta_start: beginning of the interval for valid thetas in radians
            phi_start: beginning of the interval for valid phis in radians
            theta_end: end of the interval for valid thetas in radians
            phi_end: beginning of the interval for valid phis in radians
        """
        if theta_start < theta_end:
            self.theta_start = theta_start
            self.theta_end = theta_end
        else:
            self.theta_start = theta_end
            self.theta_end = theta_start

        if phi_start < phi_end:
            self.phi_start = phi_start
            self.phi_end = phi_end
        else:
            self.phi_start = phi_end
            self.phi_end = phi_start

        if not (0 <= self.theta_start <= self.theta_end <= pi):
            raise ValueError("allowed range for theta is [0, pi]")

        if not (0 <= self.phi_start <= self.phi_end <= 2*pi):
            raise ValueError("allowed range for phi is [0, 2pi]")


class DegreeRange(QubitRange):
    """
    specify possible qubit states with use of hopf coordinates and degrees
    """
    def __init__(
            self, theta_start: float, phi_start: float,
            theta_end: float, phi_end: float) -> None:
        """
        initialize
        Args:
            theta_start: beginning of the interval for valid thetas in degrees
            phi_start: beginning of the interval for valid phis in degrees
            theta_end: end of the interval for valid thetas in degrees
            phi_end: beginning of the interval for valid phis in degrees
        """
        theta_in_radians_start = radians(theta_start)
        phi_in_radians_start = radians(phi_start)
        theta_in_radians_end = radians(theta_end)
        phi_in_radians_end = radians(phi_end)

        super().__init__(theta_in_radians_start, phi_in_radians_start,
                         theta_in_radians_end, phi_in_radians_end)


class AnyRange(QubitRange):
    """
    specify possible qubit states to any valid qubit state
    """
    def __init__(self) -> None:
        """
        initialize
        """
        super().__init__(0, 0, pi, 2*pi)

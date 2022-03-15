from math import radians, pi


class QubitRange:
    def __init__(
            self, theta_start: float, phi_start: float,
            theta_end: float, phi_end: float) -> None:
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


class DegreeRange(QubitRange):
    def __init__(
            self, theta_start: float, phi_start: float,
            theta_end: float, phi_end: float) -> None:
        theta_in_radians_start = radians(theta_start)
        phi_in_radians_start = radians(phi_start)
        theta_in_radians_end = radians(theta_end)
        phi_in_radians_end = radians(phi_end)

        super().__init__(theta_in_radians_start, phi_in_radians_start,
                         theta_in_radians_end, phi_in_radians_end)


class AnyRange(QubitRange):
    def __init__(self) -> None:
        super().__init__(0, 0, pi, 2*pi)

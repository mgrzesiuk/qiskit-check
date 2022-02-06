from math import radians, pi


class QubitRange:
    def __init__(
            self, angle_start: float, relative_phase_start: float,
            angle_end: float, relative_phase_end: float) -> None:
        if angle_start < angle_end:
            self.angle_start = angle_start
            self.angle_end = angle_end
        else:
            self.angle_start = angle_end
            self.angle_end = angle_start

        if relative_phase_start < relative_phase_end:
            self.relative_phase_start = relative_phase_start
            self.relative_phase_end = relative_phase_end
        else:
            self.relative_phase_start = relative_phase_end
            self.relative_phase_end = relative_phase_start


class DegreeRange(QubitRange):
    def __init__(
            self, angle_start: float, relative_phase_start: float,
            angle_end: float, relative_phase_end: float) -> None:
        angle_in_radians_start = radians(angle_start)
        relative_phase_in_radians_start = radians(relative_phase_start)
        angle_in_radians_end = radians(angle_end)
        relative_phase_in_radians_end = radians(relative_phase_end)

        super().__init__(angle_in_radians_start, relative_phase_in_radians_start,
                         angle_in_radians_end, relative_phase_in_radians_end)


class AnyRange(QubitRange):
    def __init__(self) -> None:
        super().__init__(0, 0, 2*pi, 2*pi)


class AmplitudeRange(QubitRange):
    pass  # TODO: do I want to support this? seems messy given no comparisons between complex values

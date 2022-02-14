from typing import List


class QubitResult:
    pass


class TomographyResult(QubitResult):
    pass


class MeasurementResult:
    def __init__(self, measurements: List[str]):
        self.counts = {"0": 0, "1": 0}
        for measurement in measurements:
            self.counts[measurement] += 1


class MeasurementQubitResult(QubitResult, MeasurementResult):
    pass


class BitResult(MeasurementResult):
    pass

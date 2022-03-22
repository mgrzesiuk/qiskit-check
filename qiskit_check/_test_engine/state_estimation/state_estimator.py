from typing import Optional

from qiskit_check._test_engine.concrete_property_test.test_case import TestCase
from qiskit_check._test_engine.state_estimation.tomography.abstract_tomography import AbstractTomography
from qiskit_check.property_test.test_results import TomographyResult


class StateEstimator:
    def __init__(self, tomography: AbstractTomography) -> None:
        self.tomography = tomography

    def run(self, test_case: TestCase) -> Optional[TomographyResult]:
        if not test_case.assessor.tomography_requirement.requires_tomography:
            return None
        else:
            if self.tomography is None:
                raise NoTomographyError("specified assertions require tomography "
                                        "but not tomography engine was specified")

            return self._run_test_case(test_case)

    def _run_test_case(self, test_case: TestCase) -> TomographyResult:
        pass


class NoTomographyError(ValueError):
    pass

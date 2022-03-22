from typing import Sequence

from qiskit_check.property_test.assertions import AbstractAssertion


class TomographyRequirement:
    def __init__(self, assertions: Sequence[AbstractAssertion]) -> None:
        self.qubits_requiring_tomography = set()

        for assertion in assertions:
            self.qubits_requiring_tomography.update(assertion.get_qubits_requiring_tomography())

        self.requires_tomography = (len(self.qubits_requiring_tomography) > 0)

from typing import Sequence

from qiskit_check.property_test.assertions import AbstractAssertion


class TomographyRequirement:
    def __init__(self, assertions: Sequence[AbstractAssertion]) -> None:
        self.qubits_requiring_tomography = {}
        self._parse_assertions(assertions)
        self.requires_tomography = (len(self.qubits_requiring_tomography.keys()) > 0)

    def _parse_assertions(self, assertions: Sequence[AbstractAssertion]) -> None:
        for assertion in assertions:
            qubit_requirements = assertion.get_qubits_requiring_tomography()
            for qubit, location in qubit_requirements.items():
                if qubit in self.qubits_requiring_tomography:
                    self.qubits_requiring_tomography[qubit].append(location)
                else:
                    self.qubits_requiring_tomography[qubit] = [location]

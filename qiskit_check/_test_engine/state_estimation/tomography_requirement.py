from typing import Sequence

from qiskit_check.property_test.assertions import AbstractAssertion
from qiskit_check.property_test.utils import amend_instruction_location


class TomographyRequirement:
    """
    class to compute and store which (qubit, location) pairs require tomography given assertions
    """
    def __init__(self, assertions: Sequence[AbstractAssertion]) -> None:
        """
        initialize
        Args:
            assertions: sequence of assertions
        """
        self.qubits_requiring_tomography = {}
        self._parse_assertions(assertions)
        self.requires_tomography = (len(self.qubits_requiring_tomography.keys()) > 0)

    def _parse_assertions(self, assertions: Sequence[AbstractAssertion]) -> None:
        """
        parse assertions to get qubit, location pairs that require tomography
        Args:
            assertions: sequence of assertions for the property test

        Returns: none

        """
        for assertion in assertions:
            qubit_requirements = assertion.get_qubits_requiring_tomography()
            for qubit, location in qubit_requirements.items():
                amended_location = amend_instruction_location(location)  # because initialize is an instruction
                if qubit in self.qubits_requiring_tomography:
                    self.qubits_requiring_tomography[qubit].append(amended_location)
                else:
                    self.qubits_requiring_tomography[qubit] = [amended_location]

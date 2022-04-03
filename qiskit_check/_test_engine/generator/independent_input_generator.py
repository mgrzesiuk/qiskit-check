from abc import abstractmethod
from typing import Sequence, List

from qiskit.quantum_info import Statevector

from qiskit_check._test_engine.generator import QubitInputGenerator
from qiskit_check.property_test.resources import Qubit


class IndependentInputGenerator(QubitInputGenerator):
    def generate(self, qubits: Sequence[Qubit]) -> List[Statevector]:
        """
        generate initial state for qubits
        Args:
            qubits: sequence of qubits for which to generate initial values

        Returns: sequence of qiskit Statevectors which are to be initial values for qubits (respectively to position
        of qubits in the input sequence)

        """
        return [self._generate_single_value(qubit) for qubit in qubits]

    @staticmethod
    @abstractmethod
    def _generate_single_value(qubit: Qubit) -> Statevector:
        """
        generate initial state for single qubit
        Args:
            qubit: qubit for which to generate initial state

        Returns: qiskit Statevector describing initial state of the qubit

        """
        pass

import uuid
from qiskit.quantum_info import Statevector

from qiskit_check.property_test.resources.qubit_range import QubitRange


class Qubit:
    """
    class used as a template for real qubit, this lets user specify the possible initial states of the qubit
    """
    def __init__(self, values: QubitRange):
        """
        initialize
        Args:
            values: possible initial states of the qubit
            name: name of the qubit, used to identify it (if two qubits have the same name they will be considered equal)
        """
        self.values = values
        self.name = str(uuid.uuid4())
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Qubit) and self.name == other.name
    
    def __hash__(self) -> int:
        return hash(self.name)


class ConcreteQubit:
    """
    class holding information about concrete implementation of a Qubit like its initial state and its index in
    the circuit that has been run as part of the test
    """
    def __init__(self, qubit_index: int, value: Statevector) -> None:
        """
        initialize
        Args:
            qubit_index: index of the qubit in QuantumCircuit that has been run for tests
            value: state to which the qubit got initialized
        """
        self.qubit_index = qubit_index
        self.value = value

    def get_qubit(self) -> int:
        """
        get index of the qubit in QuantumCircuit run for tests
        Returns: index of the qubit in respective QuantumCircuit

        """
        return self.qubit_index

    def get_initial_value(self) -> Statevector:
        """
        get initial state of the qubit
        Returns: state to which the qubit got initialized

        """
        return self.value

from qiskit import QuantumCircuit

from case_studies.fourier_transform.src import qft
from case_studies.fourier_transform.tst import AbstractFourierInverseAndFourierGiveIdentityProperty


class MutationNoInverseFourierIQFTAndFourierGiveIdentityProperty(AbstractFourierInverseAndFourierGiveIdentityProperty):
    @property
    def circuit(self) -> QuantumCircuit:
        number_qubits = len(self.qubits)
        test_circuit = qft(number_qubits)
        test_circuit.measure_all()
        return test_circuit


class MutationNoQFTFourierInverseAndFourierGiveIdentityProperty(AbstractFourierInverseAndFourierGiveIdentityProperty):
    @property
    def circuit(self) -> QuantumCircuit:
        number_qubits = len(self.qubits)
        test_circuit = qft(number_qubits).inverse()
        test_circuit.measure_all()
        return test_circuit


class MutationAddXFourierInverseAndFourierGiveIdentityProperty(AbstractFourierInverseAndFourierGiveIdentityProperty):
    @property
    def circuit(self) -> QuantumCircuit:
        number_qubits = len(self.qubits)
        test_circuit = qft(number_qubits)
        for qubit in test_circuit.qubits:
            test_circuit.x(qubit)
        test_circuit = test_circuit.compose(qft(number_qubits).inverse())
        test_circuit.measure_all()
        return test_circuit


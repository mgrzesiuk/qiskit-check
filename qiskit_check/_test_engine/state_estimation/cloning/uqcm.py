from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Qubit

from qiskit_check._test_engine.state_estimation.cloning.abstract_cloner import AbstractCloner


class UQCM(AbstractCloner):
    def get_circuit(self, circuit: QuantumCircuit, qubit: Qubit, location: int) -> QuantumCircuit:
        qreg = QuantumRegister(2, name="cloner")
        circuit.add_register(qreg)
        cloning_instruction = self._get_instruction()
        parsed_instruction = (cloning_instruction, [qubit, *qreg], [])
        circuit.data.insert(location, parsed_instruction)
        return circuit

    def _get_instruction(self) -> QuantumCircuit:
        circuit = QuantumCircuit(3)


        return circuit.to_instruction()

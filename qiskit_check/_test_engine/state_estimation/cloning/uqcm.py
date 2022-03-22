from math import acos, sqrt
from typing import Tuple

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Qubit, Instruction

from qiskit_check._test_engine.state_estimation.cloning.abstract_cloner import AbstractCloner


class UniversalQuantumCopyMachine(AbstractCloner):
    def get_circuit(
            self, circuit: QuantumCircuit, qubit: Qubit,
            location: int, uid: str) -> Tuple[QuantumCircuit, QuantumRegister]:
        qreg = QuantumRegister(2, name=f"uqcm_{uid}")
        circuit.add_register(qreg)
        cloning_instruction = self._get_instruction(uid)
        parsed_instruction = (cloning_instruction, [qubit, *qreg], [])
        circuit.data.insert(location, parsed_instruction)
        return circuit, qreg

    @staticmethod
    def _get_instruction(uid: str) -> Instruction:
        circuit = QuantumCircuit(3)
        circuit.ry(acos(1/sqrt(5)), 1)
        circuit.cx(1, 2)
        circuit.ry(acos(sqrt(5)/3), 2)
        circuit.cx(2, 1)
        circuit.ry(acos(2/sqrt(5)), 1)
        circuit.cx(0, 1)
        circuit.cx(0, 2)
        circuit.cx(1, 0)
        circuit.cx(2, 0)
        return circuit.to_instruction(label=f"uqcm_{uid}")

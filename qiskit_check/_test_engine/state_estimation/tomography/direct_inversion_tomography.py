from typing import Tuple, Dict
from uuid import uuid4

from qiskit import QuantumCircuit, ClassicalRegister
from qiskit.circuit import Instruction
from qiskit_utils import insert_instruction

from qiskit_check._test_engine.state_estimation.tomography import AbstractTomography


class DirectInversionTomography(AbstractTomography):
    """
    https://arxiv.org/pdf/quant-ph/0407197.pdf?fbclid=IwAR1h4yn53Popl9PbyY1p7BPeGB51hMhqQTT9SZknGcKziRDU34Y5fpX5IfI
    """
    def insert_measurement(
            self, circuit: QuantumCircuit, qubit_index: int,
            location: int, measurement: Instruction) -> None:
        # remove all other measurements of the qubit
        amended_location = location
        instructions_to_delete = []
        for instruction, qubits, bits in circuit.get_instructions("measure"):
            if qubit_index == qubits[0].register.index(qubits[0]):
                instructions_to_delete.append((instruction, qubits, bits))

        for instruction in instructions_to_delete:
            measurement_location = circuit.data.index(instruction)
            circuit.data.remove(instruction)
            if measurement_location < location:
                amended_location -= 1

        creg = ClassicalRegister(1, name=self._get_cregs_name())
        circuit.add_register(creg)
        insert_instruction(circuit, measurement, (qubit_index, ), (creg[0], ), amended_location)

    def estimate_state(self, measurements: Dict[str, Dict[str, int]]) -> Tuple[float, float, float]:
        p_z = measurements["z"]["1"]/(measurements["z"]["0"] + measurements["z"]["1"])
        p_y = measurements["y"]["1"]/(measurements["y"]["0"] + measurements["y"]["1"])
        p_x = measurements["x"]["1"]/(measurements["x"]["0"] + measurements["x"]["1"])

        x = -1*(2 * p_x - 1)
        y = 2 * p_y - 1
        z = 1 - 2 * p_z

        return x, y, z

    @staticmethod
    def _get_cregs_name() -> str:
        return f"tomography-{uuid4().__str__()}"

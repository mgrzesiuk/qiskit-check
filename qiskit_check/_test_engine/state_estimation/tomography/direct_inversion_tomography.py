from typing import Tuple, Dict
from uuid import uuid4

from qiskit import QuantumCircuit, ClassicalRegister
from qiskit.circuit import Instruction
from qiskit_utils import insert_instruction

from qiskit_check._test_engine.state_estimation.tomography import AbstractTomography


class DirectInversionTomography(AbstractTomography):
    """
    direct inversion technic according to:
    https://arxiv.org/pdf/quant-ph/0407197.pdf?fbclid=IwAR1h4yn53Popl9PbyY1p7BPeGB51hMhqQTT9SZknGcKziRDU34Y5fpX5IfI
    """
    def insert_measurement(
            self, circuit: QuantumCircuit, qubit_index: int,
            location: int, measurement: Instruction) -> None:
        """
        insert measurement at a given location for a given qubit in q circuit - this method removes all other
        measurements for the qubit, due to qiskit simulator letting modify already measured qubits and hence breaking
        parsing of results
        Args:
            circuit: circuit where to insert the measurement
            qubit_index: index of qubit to measure
            location: desired location of the measurement (index of inserted measurement in circuit.data)
            measurement: instruction to insert

        Returns: None, insertion done in place

        """

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
        """
        get estimate of bloch vector given measurements
        Args:
            measurements: measurements with dict {'x': counts in x basis, 'y': counts in y basis, 'z' counts in z basis}

        Returns: [x,y,z] - estimated bloch vector

        """
        p_z = measurements["z"]["1"]/(measurements["z"]["0"] + measurements["z"]["1"])
        p_y = measurements["y"]["1"]/(measurements["y"]["0"] + measurements["y"]["1"])
        p_x = measurements["x"]["1"]/(measurements["x"]["0"] + measurements["x"]["1"])

        x = 1 - 2 * p_x
        y = 2 * p_y - 1
        z = 1 - 2 * p_z

        return x, y, z

    @staticmethod
    def _get_cregs_name() -> str:
        """
        get unique name for added classical registers
        Returns: unique name for classical register

        """
        return f"tomography-{uuid4().__str__()}"

from collections import Sequence
from typing import Dict, Tuple

from qiskit.result import Result

from qiskit_check.property_test.test_results import QubitResult, BitResult, MeasurementQubitResult


class TestResult:
    def __init__(
            self, num_qubits: int, num_bits: int, qubit_results: Sequence[QubitResult],
            bit_results: Sequence[BitResult], qiskit_result: Result) -> None:
        self.num_qubits = num_qubits
        self.num_qubits = num_bits
        self.qubit_results = qubit_results
        self.bit_results = bit_results
        self.qiskit_result = qiskit_result

    def get_qubit_result(self, qubit_index: int) -> QubitResult:
        return self.qubit_results[qubit_index]

    def get_bit_result(self, bit_index: int) -> BitResult:
        return self.bit_results[bit_index]

    @staticmethod
    def from_qiskit_result(result: Result):
        num_qubits = result.results[0].header.n_qubits
        num_bits = 0
        for classical_reg in result.results[0].header.creg_sizes:
            num_bits += int(classical_reg[1])

        qubit_results, bit_results = TestResult._get_resource_results(num_qubits, num_bits, result.get_counts())

        return TestResult(num_qubits, num_bits, qubit_results, bit_results, result)

    @staticmethod
    def _get_resource_results(
            num_qubits: int, num_bits: int,
            counts: Dict[str, int]) -> Tuple[Sequence[QubitResult], Sequence[BitResult]]:
        # TODO: this needs a redesign
        qubit_results = []

        for _ in range(num_qubits):
            qubit_results.append(MeasurementQubitResult([]))

        bit_results = []

        for _ in range(num_bits):
            bit_results.append(BitResult([]))

        for states, values in counts:
            registers = states.split(" ")
            quantum_register = registers[0]
            for i in range(len(qubit_results)):
                qubit_results[i].value.append(quantum_register[num_qubits - i - 1])

            if num_bits > 0:
                bit_register = "".join(registers[1:])
                for i in range(len(bit_results)):
                    bit_results[i].value.append(bit_register[num_qubits - i - 1])

        return qubit_results, bit_results

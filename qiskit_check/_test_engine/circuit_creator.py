from copy import deepcopy
from typing import Dict, List, Set, Tuple, Union
from uuid import uuid4

from qiskit import ClassicalRegister, QuantumCircuit
from qiskit.circuit import Instruction
from qiskit_utils import insert_instruction


from qiskit_check._test_engine.concrete_property_test.test_case import TestCase
from qiskit_check.property_test.resources.test_resource import ConcreteQubit, Qubit


class CircuitCreator:
    def get_circuits(self, test_case: TestCase) -> Tuple[Dict[str, List[str]], Dict[str, QuantumCircuit]]:
        measurement_locations = deepcopy(test_case.assessor.measurement_locations)
        circuits = {}
        circuit_names = {}
        updated = True
        while updated:
            updated = False
            added_qubits = set()
            circuit = test_case.circuit.copy()
            for qubits in measurement_locations.keys():
                if not self._can_be_inserted(qubits, added_qubits):
                    continue
                if len(measurement_locations[qubits]) == 0:
                    continue

                measurement_location = measurement_locations[qubits].pop()
                encoding = test_case.assessor.encode_measurement(qubits, measurement_location.location, measurement_location.instruction)
                 # we need to account for initialization of qubits (1 per qubit)
                amended_location = len(circuit.qubits) + measurement_location.location if measurement_location.location is not None else None
                circuit = self._insert_measurements(qubits, circuit, measurement_location.instruction, amended_location, test_case.assessor.resource_matcher)
                updated = True
                added_qubits.update(qubits)

                if circuit.name in circuits:
                    circuits[circuit.name].append(encoding)
                else:
                    circuits[circuit.name] = [encoding]
                    circuit_names[circuit.name] = circuit
        return circuits, circuit_names

    def _insert_measurements(
            self, qubits: Tuple[Qubit], circuit: QuantumCircuit, instruction: Instruction,
            location: Union[int, None], resource_matcher: Dict[Qubit, ConcreteQubit]) -> QuantumCircuit:

        for qubit in qubits:
            cl_reg = ClassicalRegister(1)
            circuit.add_register(cl_reg)
            location = len(circuit.data) if location is None else location
            circuit = insert_instruction(circuit, instruction, [resource_matcher[qubit].qubit_index], cl_reg, location)
        circuit.name = str(uuid4())
        return circuit

    def _can_be_inserted(self, qubits_to_add: Tuple[Qubit], added_qubits: Set[Qubit]) -> bool:
        for qubit in qubits_to_add:
            if qubit in added_qubits:
                return False
        
        return True

from random import uniform
from typing import List, Sequence

from qiskit.quantum_info import Statevector

from qiskit_check._test_engine.generator.input_generator.abstract_input_generator import QubitInputGeneratorFactory
from qiskit_check._test_engine.generator.input_generator.abstract_input_generator import QubitInputGenerator
from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.utils import hopf_coordinates_to_vector_state


class UniformInputGenerator(QubitInputGenerator):
    def generate(self, qubits: Sequence[Qubit]) -> List[Statevector]:
        return [self._generate_single_value(qubit) for qubit in qubits]

    @staticmethod
    def _generate_single_value(qubit: Qubit) -> Statevector:
        angle = uniform(qubit.values.angle_start, qubit.values.angle_end)
        relative_phase = uniform(qubit.values.relative_phase_start, qubit.values.relative_phase_end)
        ground_state_amp, excited_state_amp = hopf_coordinates_to_vector_state(angle, relative_phase)
        return Statevector([ground_state_amp, excited_state_amp])


class UniformInputGeneratorFactory(QubitInputGeneratorFactory):
    def build(self) -> QubitInputGenerator:
        return UniformInputGenerator()

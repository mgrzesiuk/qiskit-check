from numpy.random import uniform
from qiskit.quantum_info import Statevector

from qiskit_check._test_engine.generator.abstract_input_generator import QubitInputGeneratorFactory
from qiskit_check._test_engine.generator.abstract_input_generator import QubitInputGenerator
from qiskit_check._test_engine.generator.independent_input_generator import IndependentInputGenerator
from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.utils import hopf_coordinates_to_vector_state


class NaiveInputGenerator(IndependentInputGenerator):
    @staticmethod
    def _generate_single_value(qubit: Qubit) -> Statevector:
        theta = uniform(qubit.values.theta_start, qubit.values.theta_end)
        phi = uniform(qubit.values.phi_start, qubit.values.phi_end)
        ground_state_amp, excited_state_amp = hopf_coordinates_to_vector_state(theta, phi)
        return Statevector([ground_state_amp, excited_state_amp])


class NaiveInputGeneratorFactory(QubitInputGeneratorFactory):
    def build(self) -> QubitInputGenerator:
        return NaiveInputGenerator()

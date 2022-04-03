from numpy.random import uniform
from qiskit.quantum_info import Statevector

from qiskit_check._test_engine.generator.abstract_input_generator import QubitInputGeneratorFactory
from qiskit_check._test_engine.generator.abstract_input_generator import QubitInputGenerator
from qiskit_check._test_engine.generator.independent_input_generator import IndependentInputGenerator
from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.utils import hopf_coordinates_to_vector_state


class NaiveInputGenerator(IndependentInputGenerator):
    """
    generate inputs naively (both theta and phi are selected uniformly) this leads to more data being generated
    near north and south poles of the bloch sphere
    """
    @staticmethod
    def _generate_single_value(qubit: Qubit) -> Statevector:
        """
        generate initial state for qubits
        Args:
            qubits: sequence of qubits for which to generate initial values

        Returns: sequence of qiskit Statevectors which are to be initial values for qubits (respectively to position
        of qubits in the input sequence)

        """
        theta = uniform(qubit.values.theta_start, qubit.values.theta_end)
        phi = uniform(qubit.values.phi_start, qubit.values.phi_end)
        ground_state_amp, excited_state_amp = hopf_coordinates_to_vector_state(theta, phi)
        return Statevector([ground_state_amp, excited_state_amp])


class NaiveInputGeneratorFactory(QubitInputGeneratorFactory):
    """
    class for creating NaiveInputGenerator objects
    """
    def build(self) -> QubitInputGenerator:
        """
        create NaiveInputGenerator object
        Returns: NaiveInputGenerator object

        """
        return NaiveInputGenerator()

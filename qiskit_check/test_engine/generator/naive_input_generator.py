from numpy.random import uniform
from qiskit.quantum_info import Statevector

from qiskit_check.property_test.property_test_errors import InitialStateGenerationError
from qiskit_check.test_engine.generator.abstract_input_generator import QubitInputGeneratorFactory
from qiskit_check.test_engine.generator.abstract_input_generator import QubitInputGenerator
from qiskit_check.test_engine.generator.independent_input_generator import IndependentInputGenerator
from qiskit_check.property_test.resources.test_resource import Qubit
from qiskit_check.property_test.utils import hopf_coordinates_to_vector_state


class NaiveInputGenerator(IndependentInputGenerator):
    """
    generate inputs naively (both theta and phi are selected uniformly) this leads to more data being generated
    near north and south poles of the bloch sphere
    """
    def _generate_single_value(self, qubit: Qubit) -> Statevector:
        """
        generate initial state for qubits
        Args:
            qubit: sequence of qubits for which to generate initial values

        Returns: sequence of qiskit Statevectors which are to be initial values for qubits (respectively to position
        of qubits in the input sequence)

        """
        for _ in range(self.tolerance):
            theta = uniform(qubit.values.theta_start, qubit.values.theta_end)
            phi = uniform(qubit.values.phi_start, qubit.values.phi_end)
            ground_state_amp, excited_state_amp = hopf_coordinates_to_vector_state(theta, phi)
            possible_state_vector = Statevector([ground_state_amp, excited_state_amp])
            if self.state_filter(possible_state_vector):
                return possible_state_vector

        raise InitialStateGenerationError("could not generate a state vector satisfying provided filter")


class NaiveInputGeneratorFactory(QubitInputGeneratorFactory):
    """
    class for creating NaiveInputGenerator objects
    """
    def build(self) -> QubitInputGenerator:
        """
        create NaiveInputGenerator object
        Returns: NaiveInputGenerator object

        """
        return NaiveInputGenerator(self.state_filter, self.tolerance)

from math import asin, sin, sqrt

from numpy.random import uniform
from qiskit.quantum_info import Statevector

from qiskit_check.property_test.property_test_errors import InitialStateGenerationError
from qiskit_check.test_engine.generator import QubitInputGenerator, QubitInputGeneratorFactory
from qiskit_check.test_engine.generator.independent_input_generator import IndependentInputGenerator
from qiskit_check.property_test.resources import Qubit
from qiskit_check.property_test.utils import hopf_coordinates_to_vector_state

"""
https://eprint.iacr.org/2019/1204.pdf
https://pennylane.ai/qml/demos/tutorial_haar_measure.html#show-me-more-math
https://arxiv.org/pdf/1404.1444.pdf
http://home.lu.lv/~sd20008/papers/essays/Random%20unitary%20[paper].pdf
https://arxiv.org/pdf/math-ph/0609050.pdf
https://statweb.stanford.edu/~cgates/PERSI/papers/subgroup-rand-var.pdf
https://reader.elsevier.com/reader/sd/pii/S0047259X05000382?token=198945D6C08736B31B46E1DACAF74CE78246A33DE2DD9D621C637662A1ED2E5B1ADCEA09F3B4E0E660F1421686C1A9DE&originRegion=eu-west-1&originCreation=20220315135152
"""


class HaarInputGenerator(IndependentInputGenerator):
    """
    generate inputs uniformly according to haar measure
    """
    def _generate_single_value(self, qubit: Qubit) -> Statevector:
        """
        generate initial state for qubits
        Args:
            qubits: sequence of qubits for which to generate initial values

        Returns: sequence of qiskit Statevectors which are to be initial values for qubits (respectively to position
        of qubits in the input sequence)

        """
        for _ in range(self.tolerance):
            unif_lower_bound = sin(qubit.values.theta_start/2)**2
            unif_upper_band = sin(qubit.values.theta_end/2)**2

            unif_generating_theta = uniform(unif_lower_bound, unif_upper_band)
            theta = 2*asin(sqrt(unif_generating_theta))
            phi = uniform(qubit.values.phi_start, qubit.values.phi_end)
            ground_state_amp, excited_state_amp = hopf_coordinates_to_vector_state(theta, phi)
            generated = Statevector([ground_state_amp, excited_state_amp])
            if self.state_filter(generated):
                return generated

        raise InitialStateGenerationError("could not generate a state vector satisfying provided filter")


class HaarInputGeneratorFactory(QubitInputGeneratorFactory):
    """
    class for creating HaarInputGenerator objects
    """
    def build(self) -> QubitInputGenerator:
        """
        create HaarInputGenerator object
        Returns: HaarInputGenerator object

        """
        return HaarInputGenerator(self.state_filter, self.tolerance)

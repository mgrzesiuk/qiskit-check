from typing import Sequence, Tuple, List, Callable

from numpy import ndarray, asarray, cos, sin, dot, arccos, linspace
from numpy import float as npfloat
from math import fmod, pi
from numpy.random import choice
from qiskit.quantum_info import Statevector

from qiskit_check.property_test.property_test_errors import InitialStateGenerationError
from qiskit_check.test_engine.generator.abstract_input_generator import QubitInputGeneratorFactory
from qiskit_check.test_engine.generator.abstract_input_generator import QubitInputGenerator
from qiskit_check.property_test.resources import Qubit, QubitRange
from qiskit_check.property_test.utils import vector_state_to_hopf_coordinates


class NaiveDistanceInputGenerator(QubitInputGenerator):
    """
    class for generating qubits in such way that qubits further away from already generated qubits (distance measured
     between qubits generated from the same template - for one qubit in quantum circuit) is more likely to be generated
    """
    def __init__(
            self,single_qubit_generator_factory: QubitInputGeneratorFactory, quantization_rate: int,
            state_filter: Callable[[Statevector], bool] = lambda x: True, tolerance: int = 100) -> None:
        """
        initialize
        Args:
            single_qubit_generator_factory: qubit input generator for one qubit, used when all states are equally likely
            (when no qubits were generated or when generating in a one of the buckets that was created during
            quantization of the bloch sphere)
            quantization_rate: positive integer to specify how many buckets to separate bloch sphere into
            state_filter: function to filter out statevectors that are not allowed as initial states
            tolerance: num tries of generating statevector that satisfies state_filter, if exceeded and state_filter
            does not return true for any of generated statevectors error is thrown
        """
        super().__init__(state_filter)
        self.specific_generators = []
        self.uniform_generator = single_qubit_generator_factory.build()
        self.quantization_rate = quantization_rate
        self.state_filter = state_filter
        self.tolerance = tolerance

    def generate(self, qubits: Sequence[Qubit]) -> List[Statevector]:
        """
        generate initial state for qubits
        Args:
            qubits: sequence of qubits for which to generate initial values

        Returns: sequence of qiskit Statevectors which are to be initial values for qubits (respectively to position
        of qubits in the input sequence)

        """
        if len(self.specific_generators) == 0:
            return self._generate_first_time(qubits)
        generated_qubits = []
        for i in range(len(qubits)):
            qubit = qubits[i]
            if qubit.values.phi_start == qubit.values.phi_end and qubit.values.theta_start == qubit.values.theta_end:
                generated_qubits.append(self.uniform_generator.generate([qubit])[0])
            else:
                generated_qubits.append(self.specific_generators[i].generate())
        return generated_qubits

    def _generate_first_time(self, qubits: Sequence[Qubit]) -> List[Statevector]:
        """
        generate qubits for the first time with use of qubit generator specified in the constructor
        Args:
            qubits: qubits to generate

        Returns: list of state vectors with initial values of qubits

        """
        generated_qubits = self.uniform_generator.generate(qubits)
        self._initialize_specific_generators(qubits, generated_qubits)
        return generated_qubits

    def _initialize_specific_generators(self, qubits: Sequence[Qubit], generated_qubits: List[Statevector]) -> None:
        """
        initialize distance generators for each qubit template
        Args:
            qubits: qubit templates for which to initialize distance generators
            generated_qubits: list of first values generated (with generator from constructor)

        Returns: None

        """
        for generated_qubit, template_qubit in zip(generated_qubits, qubits):
            hopf_coordinates_qubit = vector_state_to_hopf_coordinates(*generated_qubit.data)
            specific_generator = NaiveDistanceSingleInputGenerator(template_qubit, hopf_coordinates_qubit,
                                                                   self.quantization_rate, self.uniform_generator,
                                                                   self.state_filter, self.tolerance)
            self.specific_generators.append(specific_generator)


class NaiveDistanceSingleInputGenerator:
    """
    generator to generate qubits based on distance to all previously generated qubits
    """
    def __init__(
            self, qubit: Qubit, initial_generation: Tuple[float, float],
            quantization_rate: float, uniform_generator:  QubitInputGenerator,
            state_filter: Callable[[Statevector], bool] = lambda x: True, tolerance: int = 100) -> None:
        """
        initialize
        Args:
            qubit: qubit template for this distance generator
            initial_generation: first state that was generated for this qubit template
            quantization_rate: positive integer to specify how many buckets to separate bloch sphere into
            uniform_generator: qubit input generator for one qubit, used when all states are equally likely
            (when generating in a one of the buckets that was created during quantization of the bloch sphere)
            state_filter: function to filter out statevectors that are not allowed as initial states
            tolerance: num tries of generating statevector that satisfies state_filter, if exceeded and state_filter
            does not return true for any of generated statevectors error is thrown
        """
        self.qubit = qubit
        self.quantization_rate = quantization_rate
        self.uniform_generator = uniform_generator
        self.previously_generated = [initial_generation]
        self.buckets, self.weights, self.weights_sum = self._get_buckets(qubit)
        self.state_filter = state_filter
        self.tolerance = tolerance

    def generate(self) -> Statevector:
        """
        generate initial state for qubit template based on previously generated values
        Returns: initial qubit state

        """
        for _ in range(self.tolerance):
            bucket_probabilities = self._get_normalized_weights()
            chosen_bucket_index = choice(len(self.buckets), p=bucket_probabilities)
            chosen_bucket = self.buckets[chosen_bucket_index]

            bucket_theta_size = self.qubit.values.theta_end - self.qubit.values.theta_start
            bucket_theta_start = fmod(chosen_bucket[0] - bucket_theta_size/self.quantization_rate, pi)
            bucket_theta_end = fmod(chosen_bucket[0] + bucket_theta_size/self.quantization_rate, pi)

            bucket_phi_size = self.qubit.values.phi_end - self.qubit.values.phi_start
            bucket_phi_start = fmod(chosen_bucket[1] - bucket_phi_size/self.quantization_rate, 2*pi)
            bucket_phi_end = fmod(chosen_bucket[1] + bucket_phi_size/self.quantization_rate, 2*pi)

            bucket_qubit = Qubit(QubitRange(bucket_theta_start, bucket_phi_start, bucket_theta_end, bucket_phi_end))
            generated_qubit = self.uniform_generator.generate([bucket_qubit])[0]
            if self.state_filter(generated_qubit):
                self._add_record_new_qubit(generated_qubit)
                return generated_qubit

        raise InitialStateGenerationError("could not generate a state vector satisfying provided filter")

    def _get_buckets(self, qubit: Qubit) -> Tuple[List[Tuple[float, float]], ndarray, float]:
        """
        split bloch sphere into multiple "buckets"
        Args:
            qubit: qubit template for which this generator is aimed

        Returns:
            list of buckets
            array of weights of the buckets (distance to the closest already generated qubit)
            sum of weights

        """
        buckets = []
        weights = []
        weights_sum = 0
        theta_start = qubit.values.theta_start
        theta_end = qubit.values.theta_end
        phi_start = qubit.values.phi_start
        phi_end = qubit.values.phi_end

        t_start = theta_start + (theta_end - theta_start)/self.quantization_rate
        p_start = phi_start + (phi_end - phi_start)/self.quantization_rate
        for theta in linspace(t_start, theta_end, num=self.quantization_rate, endpoint=True):
            for phi in linspace(p_start, phi_end, num=self.quantization_rate, endpoint=True):
                bucket = (theta, phi)
                buckets.append(bucket)
                minimal_distance = self._get_minimal_spherical_distance(bucket)
                weights_sum += minimal_distance
                weights.append(minimal_distance)

        return buckets, asarray(weights, dtype=npfloat), weights_sum

    def _get_minimal_spherical_distance(self, bucket: Tuple[float, float]) -> float:
        """
        calculate the smallest squared spherical distance between bucket and already generated initial states
        Args:
            bucket: bucket for which to calculate spherical distance

        Returns: smallest spherical distance between bucket and already generated initial states

        """
        minimal_distance = float('inf')
        bloch_vector_of_bucket = self._get_bloch_vector(*bucket)
        for point in self.previously_generated:
            bloch_vector_of_point = self._get_bloch_vector(*point)
            distance = self._get_spherical_distance_squared(bloch_vector_of_bucket, bloch_vector_of_point)
            if distance < minimal_distance:
                minimal_distance = distance
        return minimal_distance

    def _add_record_new_qubit(self, generated_qubit: Statevector) -> None:
        """
        store newly generated initial state
        Args:
            generated_qubit: newly generated initial state

        Returns: None

        """
        generated_point = self._get_bloch_vector(*vector_state_to_hopf_coordinates(*generated_qubit.data))
        for i in range(len(self.weights)):
            bucket = self._get_bloch_vector(*self.buckets[i])
            distance = self._get_spherical_distance_squared(bucket, generated_point)
            if distance < self.weights[i]:
                self.weights_sum -= (self.weights[i] - distance)
                self.weights[i] = distance

    def _get_normalized_weights(self) -> ndarray:
        """
        get array of weights that sums to 1
        Returns: array of weights (self.weights) but normalized (sums to 1)

        """
        return self.weights / self.weights_sum

    @staticmethod
    def _get_spherical_distance_squared(tested_point: ndarray, stored_point: ndarray) -> float:
        """
        get squared spherical distance between 2 points on bloch sphere
        Args:
            tested_point: bloch vector of 1st point
            stored_point: bloch vector of 1st point

        Returns: spherical distance between tested_point and stored_point

        """
        return arccos(dot(tested_point, stored_point))**2

    @staticmethod
    def _get_bloch_vector(theta: float, phi: float) -> ndarray:
        """
        calculate bloch vector from hopf coordinates
        Args:
            theta:
            phi:

        Returns: 3 dimensional bloch vector

        """
        return asarray([cos(phi)*sin(theta), sin(phi)*sin(theta), cos(theta)])


class NaiveDistanceInputGeneratorFactory(QubitInputGeneratorFactory):
    """
    factory to create NaiveDistanceInputGenerator objects
    """
    def __init__(
            self, single_qubit_generator_factory: QubitInputGeneratorFactory, quantization_rate: int = 1000,
            state_filter: Callable[[Statevector], bool] = lambda x: True, tolerance: int = 100) -> None:
        """
        initialize
        Args:
            single_qubit_generator_factory: qubit input generator for one qubit, used when all states are equally likely
            (when no qubits were generated or when generating in a one of the buckets that was created during
            quantization of the bloch sphere)
            quantization_rate: positive integer to specify how many buckets to separate bloch sphere into
            state_filter: function to filter out statevectors that are not allowed as initial states
            tolerance: num tries of generating statevector that satisfies state_filter, if exceeded and state_filter
            does not return true for any of generated statevectors error is thrown
        """
        super().__init__(state_filter)
        self.single_qubit_generator_factory = single_qubit_generator_factory
        self.quantization_rate = quantization_rate
        self.state_filter = state_filter
        self.tolerance = tolerance

    def build(self) -> NaiveDistanceInputGenerator:
        """
        build new NaiveDistanceInputGenerator object
        Returns: NaiveDistanceInputGenerator object

        """
        return NaiveDistanceInputGenerator(self.single_qubit_generator_factory, self.quantization_rate, self.state_filter, self.tolerance)

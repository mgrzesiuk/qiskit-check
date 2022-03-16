from typing import Sequence, Tuple, List, Dict

from numpy import ndarray, asarray, cos, sin, dot, arccos, linspace, longdouble
from numpy.random import choice
from qiskit.quantum_info import Statevector

from qiskit_check._test_engine.generator.abstract_input_generator import QubitInputGeneratorFactory
from qiskit_check._test_engine.generator.abstract_input_generator import QubitInputGenerator
from qiskit_check._test_engine.utils import get_object_from_config
from qiskit_check.property_test.resources import Qubit, QubitRange
from qiskit_check.property_test.utils import vector_state_to_hopf_coordinates


class NaiveDistanceInputGenerator(QubitInputGenerator):
    def __init__(self, single_qubit_generator_factory: QubitInputGeneratorFactory, quantization_rate: float) -> None:
        self.specific_generators = []
        self.uniform_generator = single_qubit_generator_factory.build()
        self.quantization_rate = quantization_rate

    def generate(self, qubits: Sequence[Qubit]) -> List[Statevector]:
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
        generated_qubits = self.uniform_generator.generate(qubits)
        self._initialize_specific_generators(qubits, generated_qubits)
        return generated_qubits

    def _initialize_specific_generators(self, qubits: Sequence[Qubit], generated_qubits: List[Statevector]) -> None:
        for generated_qubit, template_qubit in zip(generated_qubits, qubits):
            hopf_coordinates_qubit = vector_state_to_hopf_coordinates(*generated_qubit.data)
            specific_generator = NaiveDistanceSingleInputGenerator(template_qubit, hopf_coordinates_qubit,
                                                                   self.quantization_rate, self.uniform_generator)
            self.specific_generators.append(specific_generator)


class NaiveDistanceSingleInputGenerator:
    def __init__(
            self, qubit: Qubit, initial_generation: Tuple[float, float],
            quantization_rate: float, uniform_generator:  QubitInputGenerator) -> None:
        self.qubit = qubit
        self.quantization_rate = quantization_rate
        self.uniform_generator = uniform_generator
        self.previously_generated = [initial_generation]
        self.buckets, self.weights, self.weights_sum = self._get_buckets(qubit)

    def generate(self) -> Statevector:
        bucket_probabilities = self._get_normalized_weights()
        chosen_bucket_index = choice(len(self.buckets), p=bucket_probabilities)
        chosen_bucket = self.buckets[chosen_bucket_index]

        bucket_theta_size = self.qubit.values.theta_end - self.qubit.values.theta_start
        bucket_theta_start = chosen_bucket[0] - bucket_theta_size/self.quantization_rate
        bucket_theta_end = chosen_bucket[0] + bucket_theta_size/self.quantization_rate

        bucket_phi_size = self.qubit.values.phi_end - self.qubit.values.phi_start
        bucket_phi_start = chosen_bucket[1] - bucket_phi_size/self.quantization_rate
        bucket_phi_end = chosen_bucket[1] + bucket_phi_size/self.quantization_rate

        bucket_qubit = Qubit(QubitRange(bucket_theta_start, bucket_phi_start, bucket_theta_end, bucket_phi_end))
        generated_qubit = self.uniform_generator.generate([bucket_qubit])[0]
        self._add_record_new_qubit(generated_qubit)
        return generated_qubit

    def _get_buckets(self, qubit: Qubit) -> Tuple[List[Tuple[float, float]], ndarray, float]:
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

        return buckets, asarray(weights, dtype=longdouble), weights_sum

    def _get_minimal_spherical_distance(self, bucket: Tuple[float, float]) -> float:
        minimal_distance = float('inf')
        bloch_vector_of_bucket = self._get_bloch_vector(*bucket)
        for point in self.previously_generated:
            bloch_vector_of_point = self._get_bloch_vector(*point)
            distance = self._get_spherical_distance_squared(bloch_vector_of_bucket, bloch_vector_of_point)
            if distance < minimal_distance:
                minimal_distance = distance
        return minimal_distance

    def _add_record_new_qubit(self, generated_qubit: Statevector) -> None:
        generated_point = self._get_bloch_vector(*vector_state_to_hopf_coordinates(*generated_qubit.data))
        for i in range(len(self.weights)):
            bucket = self._get_bloch_vector(*self.buckets[i])
            distance = self._get_spherical_distance_squared(bucket, generated_point)
            if distance < self.weights[i]:
                self.weights_sum -= (self.weights[i] - distance)
                self.weights[i] = distance

    def _get_normalized_weights(self) -> ndarray:
        return self.weights / self.weights_sum

    @staticmethod
    def _get_spherical_distance_squared(tested_point: ndarray, stored_point: ndarray) -> float:
        return arccos(dot(tested_point, stored_point))**2

    @staticmethod
    def _get_bloch_vector(theta: float, phi: float) -> ndarray:
        return asarray([cos(phi)*sin(theta), sin(phi)*sin(theta), cos(theta)])


class NaiveDistanceInputGeneratorFactory(QubitInputGeneratorFactory):
    def __init__(self, single_qubit_generator_factory_name: Dict[str, any], quantization_rate: float = 1000) -> None:
        self.single_qubit_generator_factory = get_object_from_config(single_qubit_generator_factory_name)
        self.quantization_rate = quantization_rate

    def build(self) -> NaiveDistanceInputGenerator:
        return NaiveDistanceInputGenerator(self.single_qubit_generator_factory, self.quantization_rate)

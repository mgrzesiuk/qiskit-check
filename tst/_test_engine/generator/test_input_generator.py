from math import pi

import pytest
from qiskit.quantum_info import Statevector

from qiskit_check._test_engine.generator import NaiveInputGeneratorFactory, HaarInputGeneratorFactory
from qiskit_check._test_engine.generator import NaiveDistanceInputGeneratorFactory
from qiskit_check.property_test.resources import Qubit, QubitRange, AnyRange

from qiskit_check.property_test.utils import vector_state_to_hopf_coordinates


class TestInputGenerator:
    generator_factories = [
        HaarInputGeneratorFactory(),
        NaiveDistanceInputGeneratorFactory(HaarInputGeneratorFactory(), quantization_rate=100),
        NaiveDistanceInputGeneratorFactory(NaiveInputGeneratorFactory(), quantization_rate=100),
        NaiveInputGeneratorFactory()
    ]

    @pytest.mark.parametrize("generator_factory", generator_factories)
    def test_generate_all_correct_when_multiple_qubits_with_range_specified(self, generator_factory):
        generator = generator_factory.build()
        qubits = [Qubit(QubitRange(0, pi/2, pi/2, 3*pi/4)), Qubit(QubitRange(0, pi/3, pi/4, pi/2))]
        initial_values = generator.generate(qubits)
        for initial_value, qubit in zip(initial_values, qubits):
            self.assert_in_range(qubit.values, initial_value)

    @pytest.mark.parametrize("generator_factory", generator_factories)
    def test_generate_all_correct_when_multiple_qubits_without_range_specified(self, generator_factory):
        generator = generator_factory.build()
        qubits = [Qubit(AnyRange()), Qubit(AnyRange()), Qubit(AnyRange())]
        initial_values = generator.generate(qubits)
        for initial_value, qubit in zip(initial_values, qubits):
            self.assert_in_range(qubit.values, initial_value)

    @pytest.mark.parametrize("generator_factory", generator_factories)
    def test_generate_all_correct_when_multiple_qubits_with_mix_range_specified(self, generator_factory):
        generator = generator_factory.build()
        qubits = [Qubit(QubitRange(0, pi/2, pi/2, 3*pi/4)), Qubit(QubitRange(0, pi/3, pi/4, pi/2)), Qubit(AnyRange())]
        initial_values = generator.generate(qubits)
        for initial_value, qubit in zip(initial_values, qubits):
            self.assert_in_range(qubit.values, initial_value)

    @pytest.mark.parametrize("generator_factory", generator_factories)
    def test_generate_all_correct_when_single_qubit_provided(self, generator_factory):
        generator = generator_factory.build()
        qubits = [Qubit(AnyRange())]
        initial_values = generator.generate(qubits)
        for initial_value, qubit in zip(initial_values, qubits):
            self.assert_in_range(qubit.values, initial_value)

    @pytest.mark.parametrize("generator_factory", generator_factories)
    def test_generate_does_nothing_when_no_qubits_given(self, generator_factory):
        generator = generator_factory.build()
        qubits = []
        assert len(generator.generate(qubits)) == 0

    @pytest.mark.parametrize("generator_factory", generator_factories)
    def test_generate_throws_type_error_when_not_qubit_given(self, generator_factory):
        generator = generator_factory.build()
        qubits = [generator_factory]
        with pytest.raises(AttributeError):
            generator.generate(qubits)

    @pytest.mark.parametrize("generator_factory", generator_factories)
    def test_generate_throws_type_error_when_none_given(self, generator_factory):
        generator = generator_factory.build()
        qubits = [None]
        with pytest.raises(AttributeError):
            generator.generate(qubits)

    @staticmethod
    def assert_in_range(qubit_range: QubitRange, generated_value: Statevector):
        generated_theta, generated_phi = vector_state_to_hopf_coordinates(*generated_value.data)
        assert qubit_range.theta_start <= generated_theta <= qubit_range.theta_end
        assert qubit_range.phi_start <= generated_phi <= qubit_range.phi_end

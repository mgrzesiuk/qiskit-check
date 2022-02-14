from inspect import signature
from typing import Type, Dict

from qiskit import QuantumCircuit

from qiskit_check._test_engine.assessor import Assessor, AssessorFactory
from qiskit_check._test_engine.generator.input_generator.abstract_input_generator import QubitInputGenerator
from qiskit_check.property_test.property_test import PropertyTest
from qiskit_check.property_test.property_test_errors import IncorrectPropertyTestError, ArgumentMismatchError
from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit


class TestCase:
    def __init__(
            self, circuit: QuantumCircuit, assessor: Assessor,
            num_measurements: int, num_experiments: int) -> None:
        self.circuit = circuit
        self.assessor = assessor
        self.num_measurements = num_measurements
        self.num_experiments = num_experiments


class TestCaseGenerator:
    def __init__(
            self, property_test_class: Type[PropertyTest], assessor_factory: AssessorFactory,
            qubit_input_generator: QubitInputGenerator) -> None:
        self.property_test_class = property_test_class
        self.assessor_factory = assessor_factory
        self.qubit_input_generator = qubit_input_generator

    def generate(self) -> TestCase:
        if len(signature(self.property_test_class.__init__).parameters) > 1:
            raise IncorrectPropertyTestError("Property test __init__ method can have only one argument as input")

        concrete_property_test = self.property_test_class()

        resource_matcher = self._get_resource_matcher(concrete_property_test)

        assessor = self.assessor_factory.build(concrete_property_test, resource_matcher)

        test_circuit = self._initialize_circuit(concrete_property_test.circuit, resource_matcher)
        test_circuit = self._measure_circuit(test_circuit, assessor)

        return TestCase(test_circuit, assessor, concrete_property_test.num_measurements(),
                        concrete_property_test.num_experiments())

    @staticmethod
    def _initialize_circuit(circuit: QuantumCircuit, resource_matcher: Dict[Qubit, ConcreteQubit]) -> QuantumCircuit:
        test_circuit = QuantumCircuit(len(circuit.qubits), len(circuit.clbits))

        for qubit_template, concrete_qubit in resource_matcher.items():
            test_circuit.initialize(concrete_qubit.get_initial_value(), concrete_qubit.get_qubit())

        return test_circuit + circuit

    @staticmethod
    def _measure_circuit(circuit: QuantumCircuit, assessor: Assessor) -> QuantumCircuit:
        return circuit + assessor.get_measurement_circuit(len(circuit.qubits), len(circuit.clbits))

    def _get_resource_matcher(self, concrete_property_test: PropertyTest) -> Dict[Qubit, ConcreteQubit]:
        specified_qubits = concrete_property_test.qubits
        num_specified_qubits = len(specified_qubits)

        if num_specified_qubits != len(concrete_property_test.circuit.qubits):
            raise ArgumentMismatchError(concrete_property_test)

        initial_values = self.qubit_input_generator.generate(specified_qubits)

        resource_matcher = {}
        for i in range(num_specified_qubits):
            resource_matcher[specified_qubits[i]] = ConcreteQubit(i, initial_values[i])

        return resource_matcher

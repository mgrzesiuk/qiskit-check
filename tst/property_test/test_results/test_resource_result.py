from math import sqrt

import pytest
from qiskit import Aer, QuantumCircuit, ClassicalRegister, transpile

from qiskit_check.property_test.resources import Qubit, AnyRange
from qiskit_check.property_test.test_results import TomographyResult, MeasurementResult
from qiskit_check.property_test.utils import amend_instruction_location


class TestTomographyResult:
    def test_add_result_correctly_added_when_new_qubit(self):
        qubit = Qubit(AnyRange())
        location = 4
        amended_location = amend_instruction_location(location)
        tomography_result = TomographyResult()
        vec = [1/sqrt(2), 1/sqrt(2), 0]
        tomography_result.add_result(vec, qubit, amended_location)
        assert qubit in tomography_result._estimates_storage
        assert [vec] == tomography_result._estimates_storage[qubit][amended_location]

    def test_add_result_correctly_added_when_new_location_for_qubit(self):
        qubit = Qubit(AnyRange())
        location = 4
        amended_location = amend_instruction_location(location)
        tomography_result = TomographyResult()
        vec = [1/sqrt(2), 1/sqrt(2), 0]
        tomography_result.add_result([0, 0, 1], qubit, amended_location+5)
        tomography_result.add_result(vec, qubit, amended_location)

        assert amended_location in tomography_result._estimates_storage[qubit]
        assert [vec] == tomography_result._estimates_storage[qubit][amended_location]

    def test_add_result_correctly_added_when_new_experiment_added(self):
        qubit = Qubit(AnyRange())
        location = 4
        amended_location = amend_instruction_location(location)
        tomography_result = TomographyResult()
        vec1 = [1/sqrt(2), 1/sqrt(2), 0]
        vec2 = [sqrt(5)/sqrt(3), 2/sqrt(2), 0]
        tomography_result.add_result(vec1, qubit, amended_location)
        tomography_result.add_result(vec2, qubit, amended_location)

        assert amended_location in tomography_result._estimates_storage[qubit]
        assert [vec1, vec2] == tomography_result._estimates_storage[qubit][amended_location]


    def test_add_result_correctly_added_when_new_existing_location_qubit(self):
        qubit = Qubit(AnyRange())
        location = 4
        amended_location = amend_instruction_location(location)
        tomography_result = TomographyResult()
        vec = [1/sqrt(2), 1/sqrt(2), 0]
        tomography_result.add_result([0, 0, 1], Qubit(AnyRange()), amended_location+2)
        tomography_result.add_result([0, 0, 1], qubit, amended_location+5)
        tomography_result.add_result(vec, qubit, amended_location)

        assert amended_location in tomography_result._estimates_storage[qubit]
        assert [vec] == tomography_result._estimates_storage[qubit][amended_location]

    def test_get_estimates_throws_key_error_when_not_existing_qubit(self):
        qubit = Qubit(AnyRange())
        location = 4
        tomography_result = TomographyResult()
        with pytest.raises(KeyError):
            tomography_result.get_estimates(qubit, location)

    def test_get_estimates_throws_key_error_when_not_existing_location(self):
        qubit = Qubit(AnyRange())
        location = 4
        amended_location = amend_instruction_location(location)
        tomography_result = TomographyResult()
        vec = [1/sqrt(2), 1/sqrt(2), 0]
        tomography_result.add_result(vec, qubit, amended_location)
        with pytest.raises(KeyError):
            tomography_result.get_estimates(qubit, location+1)

    def test_get_estimates_correctly_returns_when_everything_correct(self):
        qubit = Qubit(AnyRange())
        location = 4
        amended_location = amend_instruction_location(location)
        tomography_result = TomographyResult()
        vec = [1/sqrt(2), 1/sqrt(2), 0]
        tomography_result.add_result(vec, qubit, amended_location)
        assert [vec] == tomography_result.get_estimates(qubit, location)


@pytest.fixture(scope='module')
def backend():
    return Aer.get_backend("aer_simulator")


class TestMeasurementResult:
    def test_get_qubit_result_throws_value_error_when_missing_qubit(self, backend):
        circuit = QuantumCircuit(1)
        circuit.x(0)
        circuit.measure_all()
        qct = transpile(circuit, backend)
        measurement_result = MeasurementResult(backend.run(qct).result(), circuit)
        with pytest.raises(ValueError):
            measurement_result.get_qubit_result(2, "1")

    def test_get_qubit_results_returns_correct_counts_when_one_qubit(self, backend):
        circuit = QuantumCircuit(1)
        circuit.x(0)
        circuit.measure_all()
        qct = transpile(circuit, backend)
        measurement_result = MeasurementResult(backend.run(qct).result(), circuit)
        assert measurement_result.get_qubit_result(0, "1") == 1024
        assert measurement_result.get_qubit_result(0, "0") == 0

    def test_get_qubit_result_returns_correct_counts_when_multpile_qubits(self, backend):
        circuit = QuantumCircuit(2)
        circuit.x(0)
        circuit.measure_all()
        qct = transpile(circuit, backend)
        measurement_result = MeasurementResult(backend.run(qct).result(), circuit)
        assert measurement_result.get_qubit_result(0, "1") == 1024
        assert measurement_result.get_qubit_result(0, "0") == 0
        assert measurement_result.get_qubit_result(1, "0") == 1024
        assert measurement_result.get_qubit_result(1, "1") == 0

    def test_counts_parsed_no_spaces_in_keys_when_all_correct(self, backend):
        creg1 = ClassicalRegister(1)
        creg2 = ClassicalRegister(1)
        circuit = QuantumCircuit(2)
        circuit.x(0)
        circuit.add_register(creg1)
        circuit.add_register(creg2)
        circuit.measure_all()
        qct = transpile(circuit, backend)
        measurement_result = MeasurementResult(backend.run(qct).result(), circuit)
        for key in measurement_result.counts.keys():
            assert " " not in key

import pytest
from qiskit import QuantumCircuit

from qiskit_check._test_engine.state_estimation.tomography import DirectInversionTomography


class TestDirectInversionTomography:
    def test_insert_measurement_key_error_when_instruction_location_to_large(self):
        tomography = DirectInversionTomography()
        qc = QuantumCircuit(1)
        with pytest.raises(IndexError):
            tomography.insert_measurement(qc, 0, 4, tomography.get_measure_z())

    def test_insert_measurement_key_error_when_instruction_wrong_qubit(self):
        tomography = DirectInversionTomography()
        qc = QuantumCircuit(0)
        with pytest.raises(IndexError):
            tomography.insert_measurement(qc, 0, 0, tomography.get_measure_z())

    def test_insert_measurement_correctly_inserted_when_inserting_at_the_end(self):
        tomography = DirectInversionTomography()
        qc = QuantumCircuit(1)
        qc.x(0)
        tomography.insert_measurement(qc, 0, 1, tomography.get_measure_z())
        assert qc.data[1][0] == tomography.get_measure_z()

    def test_insert_measurement_correctly_inserted_when_inserting_in_middle(self):
        tomography = DirectInversionTomography()
        qc = QuantumCircuit(1)
        qc.x(0)
        qc.h(0)
        tomography.insert_measurement(qc, 0, 1, tomography.get_measure_z())
        assert qc.data[1][0] == tomography.get_measure_z()

    def test_insert_measurement_value_error_inserted_when_inserting_none(self):
        tomography = DirectInversionTomography()
        qc = QuantumCircuit(1)
        qc.x(0)
        with pytest.raises(ValueError):
            tomography.insert_measurement(qc, 0, 0, None)

    def test_estimate_state_correctly_estimates_when_correct_input_z_basis(self):
        tomography = DirectInversionTomography()
        measurements = {
            "x": {
                "1": 512,
                "0": 512,
            },
            "y": {
                "1": 512,
                "0": 512,
            },
            "z": {
                "1": 0,
                "0": 1024,
            }
        }
        assert (0, 0, 1) == tomography.estimate_state(measurements)

    def test_estimate_state_correctly_estimates_when_correct_input_y_basis(self):
        tomography = DirectInversionTomography()
        measurements = {
            "x": {
                "1": 512,
                "0": 512,
            },
            "y": {
                "1": 1024,
                "0": 0,
            },
            "z": {
                "1": 512,
                "0": 512,
            }
        }
        assert (0, 1, 0) == tomography.estimate_state(measurements)

    def test_estimate_state_correctly_estimates_when_correct_input_x_basis(self):
        tomography = DirectInversionTomography()
        measurements = {
            "x": {
                "1": 1024,
                "0": 0,
            },
            "y": {
                "1": 512,
                "0": 512,
            },
            "z": {
                "1": 512,
                "0": 512,
            }
        }
        assert (-1, 0, 0) == tomography.estimate_state(measurements)

    def test_estimate_state_correctly_arithmetic_error_when_measurements_all_0(self):
        tomography = DirectInversionTomography()
        measurements = {
            "x": {
                "1": 0,
                "0": 0,
            },
            "y": {
                "1": 0,
                "0": 0,
            },
            "z": {
                "1": 0,
                "0": 0,
            }
        }
        with pytest.raises(ArithmeticError):
            tomography.estimate_state(measurements)

    def test_estimate_state_correctly_key_error_when_no_measurements_z_basis(self):
        tomography = DirectInversionTomography()
        measurements = {
            "x": {
                "1": 1024,
                "0": 0,
            },
            "y": {
                "1": 512,
                "0": 512,
            },
        }

        with pytest.raises(KeyError):
            tomography.estimate_state(measurements)

    def test_estimate_state_correctly_key_error_when_no_measurements_x_basis(self):
        tomography = DirectInversionTomography()
        measurements = {
            "z": {
                "1": 1024,
                "0": 0,
            },
            "y": {
                "1": 512,
                "0": 512,
            },
        }

        with pytest.raises(KeyError):
            tomography.estimate_state(measurements)

    def test_estimate_state_correctly_key_error_when_no_measurements_y_basis(self):
        tomography = DirectInversionTomography()
        measurements = {
            "z": {
                "1": 1024,
                "0": 0,
            },
            "x": {
                "1": 512,
                "0": 512,
            },
        }

        with pytest.raises(KeyError):
            tomography.estimate_state(measurements)

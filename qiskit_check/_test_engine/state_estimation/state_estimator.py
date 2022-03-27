from typing import Optional, Callable, Dict

from qiskit import QuantumCircuit
from qiskit.result import Result
from qiskit_utils import parse_result

from qiskit_check._test_engine.concrete_property_test.test_case import TestCase
from qiskit_check._test_engine.state_estimation.tomography.abstract_tomography import AbstractTomography
from qiskit_check.property_test.test_results import TomographyResult


class StateEstimator:
    def __init__(self, tomography: AbstractTomography) -> None:
        self.tomography = tomography
        if self.tomography is not None:
            self.measurements = {
                "x": self.tomography.get_measure_x(),
                "y": self.tomography.get_measure_y(),
                "z": self.tomography.get_measure_z()
            }
            self.measurement_names = self.tomography.get_measurement_names()

    def run(
            self, test_case: TestCase,
            run_circuit: Callable[[QuantumCircuit, int], Result]) -> Optional[TomographyResult]:
        if not test_case.assessor.tomography_requirement.requires_tomography:
            return None
        else:
            if self.tomography is None:
                raise NoTomographyError("specified assertions require tomography "
                                        "but not tomography engine was specified")

            return self._run_test_case(test_case, run_circuit)

    def _run_test_case(
            self, test_case: TestCase, run_circuit: Callable[[QuantumCircuit, int], Result]) -> TomographyResult:
        qubits_requiring_tomography = test_case.assessor.tomography_requirement.qubits_requiring_tomography.copy()
        tomography_result = TomographyResult()
        while len(qubits_requiring_tomography.keys()) > 0:
            circuits = {measurement: test_case.circuit.copy() for measurement in self.measurements.keys()}
            circuit_specification = {}
            for qubit in list(qubits_requiring_tomography.keys()):
                location = qubits_requiring_tomography[qubit][0]
                # add tomography
                for measurement_axis, circuit in circuits.items():
                    measurement_instruction = self.measurements[measurement_axis]
                    qubit_index = test_case.assessor.resource_matcher[qubit].qubit_index
                    self.tomography.insert_measurement(circuit, qubit_index, location, measurement_instruction)
                # save which qubit-locations are checked by this circuit
                circuit_specification[qubit] = location
                # remove qubit-location combination
                qubits_requiring_tomography[qubit].remove(location)
                if len(qubits_requiring_tomography[qubit]) == 0:
                    qubits_requiring_tomography.pop(qubit)
            # run circuit
            for _ in range(test_case.num_experiments):
                experiment_results = {}
                for axis, circuit in circuits.items():
                    experiment_results[axis] = parse_result(run_circuit(circuit, test_case.num_measurements),
                                                            circuit, measurement_names=self.measurement_names)
                # parse results
                parsed_results = self._parse_results(experiment_results)
                for qubit, location in circuit_specification.items():
                    qubit_index = test_case.assessor.resource_matcher[qubit].qubit_index
                    estimated_state = self.tomography.estimate_state(parsed_results[qubit_index])
                    tomography_result.add_result(estimated_state, qubit, location)

        return tomography_result

    @staticmethod
    def _parse_results(results: Dict[str, Dict[int, Dict[str, int]]]) -> Dict[int, Dict[str, Dict[str, int]]]:
        inverted_dict = {}
        for axis, parsed_result in results.items():
            for qubit_index, counts in parsed_result.items():
                if qubit_index in inverted_dict:
                    inverted_dict[qubit_index][axis] = counts
                else:
                    inverted_dict[qubit_index] = {axis: counts}
        return inverted_dict


class NoTomographyError(ValueError):
    pass

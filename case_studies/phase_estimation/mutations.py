from qiskit import QuantumCircuit

from case_studies.phase_estimation.src import mutation_no_x_gate_phase_estimation, mutation_no_h_gate_phase_estimation
from case_studies.phase_estimation.src import mutation_no_iqft_phase_estimation
from case_studies.phase_estimation.src import mutation_additional_h_gate_phase_estimation
from case_studies.phase_estimation.tst import AbstractPhaseEstimationPropertyTest


class MutationNoXGatePhaseEstimationPropertyTest(AbstractPhaseEstimationPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_no_x_gate_phase_estimation(QuantumCircuit(len(self.qubits), 3), self.phase)


class MutationNoHGatePhaseEstimationPropertyTest(AbstractPhaseEstimationPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_no_h_gate_phase_estimation(QuantumCircuit(len(self.qubits), 3), self.phase)


class MutationNoIQFTPhaseEstimationPropertyTest(AbstractPhaseEstimationPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_no_iqft_phase_estimation(QuantumCircuit(len(self.qubits), 3), self.phase)


class MutationAddHGatePhaseEstimationPropertyTest(AbstractPhaseEstimationPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_additional_h_gate_phase_estimation(QuantumCircuit(len(self.qubits), 3), self.phase)

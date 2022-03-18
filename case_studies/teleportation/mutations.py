from qiskit import QuantumCircuit

from case_studies.teleportation.src import mutation_no_entanglement_quantum_teleportation
from case_studies.teleportation.src import mutation_no_post_update_quantum_teleportation
from case_studies.teleportation.src import mutation_no_middle_gates_quantum_teleportation
from case_studies.teleportation.tst import AbstractTeleportationProperty


class MutationNoEntanglementTeleportationProperty(AbstractTeleportationProperty):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_no_entanglement_quantum_teleportation()


class MutationNoPostUpdateTeleportationProperty(AbstractTeleportationProperty):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_no_post_update_quantum_teleportation()


class MutationNoMiddleGatesTeleportationProperty(AbstractTeleportationProperty):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_no_middle_gates_quantum_teleportation()

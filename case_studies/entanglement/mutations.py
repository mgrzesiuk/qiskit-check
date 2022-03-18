from qiskit import QuantumCircuit

from case_studies.entanglement.tst import AbstractEntanglePropertyTest


class MutationNoHEntanglePropertyTest(AbstractEntanglePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.cx(0, 1)
        qc.measure_all()
        return qc


class MutationNoCXEntanglePropertyTest(AbstractEntanglePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.measure_all()
        return qc


class MutationAdditionalCXGateEntanglePropertyTest(AbstractEntanglePropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.cx(0, 1)
        qc.measure_all()
        return qc

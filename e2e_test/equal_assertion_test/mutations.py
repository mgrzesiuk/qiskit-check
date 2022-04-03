from qiskit import QuantumCircuit

from e2e_test.equal_assertion_test.test_equal import AbstractEqualPropertyPropertyTest


class MutationXSEqualPropertyTest(AbstractEqualPropertyPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.x(0)
        qc.measure_all()
        return qc


class MutationHEqualPropertyTest(AbstractEqualPropertyPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.h(1)
        qc.measure_all()
        return qc


class MutationSEqualPropertyTest(AbstractEqualPropertyPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.s(0)
        qc.x(1)
        qc.measure_all()
        return qc


class MutationDoubleHEqualPropertyTest(AbstractEqualPropertyPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.h(0)
        qc.x(1)
        qc.measure_all()
        return qc

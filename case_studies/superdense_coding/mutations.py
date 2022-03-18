from qiskit import QuantumCircuit

from case_studies.superdense_coding.src import mutation_no_encoding_superdense_coding
from case_studies.superdense_coding.src import mutation_no_decoding_superdense_coding
from case_studies.superdense_coding.src import mutation_no_bell_pair_superdense_coding
from case_studies.superdense_coding.tst import AbstractSuperdenseCodingPropertyTest


class MutationNoBellPairSuperdenseCodingPropertyTest(AbstractSuperdenseCodingPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_no_bell_pair_superdense_coding(self.bitstring)


class MutationNoEncodingSuperdenseCodingPropertyTest(AbstractSuperdenseCodingPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_no_encoding_superdense_coding(self.bitstring)


class MutationNoDecodingSuperdenseCodingPropertyTest(AbstractSuperdenseCodingPropertyTest):
    @property
    def circuit(self) -> QuantumCircuit:
        return mutation_no_decoding_superdense_coding(self.bitstring)

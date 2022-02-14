"""
class DeutschJozsaPropertyTest(ExampleTestBase):
    def __init__(self):
        self.balanced_or_constant = random.randint(0, 1)

    @property
    def circuit(self) -> QuantumCircuit:
        return deutsch_jozsa(QuantumCircuit(4, 3), self.balanced_or_constant)

    @property
    def qubits(self) -> Collection[Qubit]:
        return [Qubit(QubitRange(0, 0, 0, 0)) for _ in range(4)]

    @property
    def bits(self) -> Collection[Bit]:

        return [Bit() for _ in range(3)]

    def evaluate_correctness(self, measurement) -> int:
        if self.balanced_or_constant == 1:
            return int(measurement == "1"*len(self.bits))
        else:
            return int(measurement == "0"*len(self.bits))

    @property
    def assertions(self) -> AbstractAssertion:
        return AssertTrue(self.evaluate_correctness, )
"""
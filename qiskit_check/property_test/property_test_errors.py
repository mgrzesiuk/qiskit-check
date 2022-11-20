

class IncorrectPropertyTestError(Exception):
    pass


class ArgumentMismatchError(IncorrectPropertyTestError):
    def __init__(self, property_test) -> None:
        test_name = property_test.__class__.__name__
        super().__init__(f"number of qubits provided in {test_name} doesn't"
                         f" match number of qubits in the provided circuit")


class IncorrectAssertionError(IncorrectPropertyTestError):
    def __init__(self, property_test) -> None:
        test_name = property_test.__class__.__name__
        super().__init__(f"assertions provided in {test_name} are not a Sequence of assertions or an assertion"
                         f"implementing qiskit_check.property_test.assertion.AbstractAssertion")


class NoQubitFoundError(IncorrectPropertyTestError):
    pass


class IncorrectQubitStateError(IncorrectPropertyTestError):
    pass


class NoExperimentsError(IncorrectPropertyTestError):
    pass


class InitialStateGenerationError(Exception):
    pass

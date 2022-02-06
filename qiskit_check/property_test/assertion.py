from abc import ABC, abstractmethod
from typing import List, Dict, Callable

from qiskit.quantum_info import Statevector
from scipy.stats import ttest_1samp, ttest_ind, ttest_rel, binomtest, fisher_exact

from qiskit_check.property_test.property_test_errors import NoQubitFoundError, IncorrectQubitStateError
from qiskit_check.property_test.property_test_errors import NoExperimentsError

from qiskit_check.property_test.resources.test_resource import Qubit, ConcreteQubit
from qiskit_check.property_test.utils import vector_state_to_hopf_coordinates, hopf_coordinates_to_vector_state


class AbstractAssertion(ABC):
    @abstractmethod
    def verify(self, experiments: List[Dict[str, int]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        """
        verify if the assertion holds
        Args:
            experiments: list of experiments made after the execution of quantum program
            resource_matcher: dictionary that matched template qubit to a index of a "real" qubit and it's initial state

        Returns: p-value of the assertion
        """
        pass

    @staticmethod
    def check_if_experiments_empty(experiments: List[Dict[str, int]]) -> None:
        if len(experiments) == 0:
            raise NoExperimentsError("no experiments have been provided")


class AssertTrue(AbstractAssertion):
    def __init__(
            self, verify_function: Callable[[Dict[str, int], Dict[Qubit, ConcreteQubit]], float],
            target_value: float) -> None:
        self.verify_function = verify_function
        self.target_value = target_value

    def verify(self, experiments: List[Dict[str, int]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        self.check_if_experiments_empty(experiments)
        experiment_values = [self.verify_function(experiment, resource_matcher) for experiment in experiments]
        return ttest_1samp(experiment_values, self.target_value).pvalue


class AssertProbability(AbstractAssertion):
    def __init__(self, qubit: Qubit, state: int, probability: float) -> None:
        self.qubit = qubit
        if state != 0 and state != 1:
            raise IncorrectQubitStateError("It is only possible to assert probability of qubit being in state 0 or 1")
        self.state = state
        self.probability = probability

    def verify(self, experiments: List[Dict[str, int]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")
        self.check_if_experiments_empty(experiments)

        qubit_index = resource_matcher[self.qubit].qubit_index
        num_shots = sum(experiments[0].values())

        num_successes = 0
        for experiment in experiments:
            for states, value in experiment.items():
                if states[qubit_index] == self.state:
                    num_successes += value
        #  TODO: this kind of ignores measurement vs experiment - what to do about this?
        return binomtest(num_successes, len(experiments) * num_shots, self.probability).pvalue


class AssertEntangled(AbstractAssertion):
    def __init__(self, qubit_0: Qubit, qubit_1: Qubit) -> None:
        self.qubit_0 = qubit_0
        self.qubit_1 = qubit_1

    def verify(self, experiments: List[Dict[str, int]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit_0 not in resource_matcher or self.qubit_1 not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(experiments)
        """
        contingency table with counts as follows:
            qubit 0 state 0 and qubit 1 in state 0 | qubit 0 in state 1 and qubit 1 in state 0
            qubit 0 state 0 and qubit 1 in state 1 | qubit 0 in state 1 and qubit 1 in state 1
        """
        contingency_table = (
            (0, 0),
            (0, 0)
        )
        qubit_0_index = resource_matcher[self.qubit_0].qubit_index
        qubit_1_index = resource_matcher[self.qubit_1].qubit_index

        for experiment in experiments:
            for states, value in experiment.items():
                qubit_0_state = int(states[qubit_0_index])
                qubit_1_state = int(states[qubit_1_index])
                contingency_table[qubit_0_state][qubit_1_state] += value

        return fisher_exact(contingency_table).p_value


class AssertEqual(AbstractAssertion):
    def __init__(self, qubit_0: Qubit, qubit_1: Qubit, ideal: bool) -> None:
        self.qubit_0 = qubit_0
        self.qubit_1 = qubit_1
        self.test = ttest_ind if ideal else ttest_rel

    def verify(self, experiments: List[Dict[str, int]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit_0 not in resource_matcher or self.qubit_1 not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(experiments)
        # TODO: this doesn't exactly check if qubits have equal states, it checks if probabilities are same,but not -|1>
        qubit_0_index = resource_matcher[self.qubit_0].qubit_index
        qubit_1_index = resource_matcher[self.qubit_1].qubit_index

        qubit_0_values = []
        qubit_1_values = []

        for experiment in experiments:
            num_qubit_0_in_state_0 = 0
            num_qubit_1_in_state_0 = 0
            for states, value in experiment.items():
                if states[qubit_0_index] == "0":
                    num_qubit_0_in_state_0 += value
                if states[qubit_1_index] == "0":
                    num_qubit_1_in_state_0 += value
            qubit_0_values.append(num_qubit_0_in_state_0)
            qubit_1_values.append(num_qubit_1_in_state_0)

        return self.test(qubit_0_values, qubit_1_values).pvalue


class AssertMostProbable(AbstractAssertion):
    def __init__(self, expected_state: str) -> None:
        self.expected_state = expected_state
        self.assert_true = AssertTrue(self._verify_function, 1)

    def _verify_function(self, experiment: Dict[str, int], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.expected_state not in experiment:
            return 0
        state_likelihood = experiment[self.expected_state]
        if state_likelihood >= max(experiment.values()):
            return 1
        else:
            return 0

    def verify(self, experiments: List[Dict[str, int]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        return self.assert_true.verify(experiments, resource_matcher)


class AssertMeasurementEqual(AbstractAssertion):
    def __init__(self, expected_state) -> None:
        self.expected_state = expected_state

    def verify(self, experiments: List[Dict[str, int]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        self.check_if_experiments_empty(experiments)

        minimal_probability = 1

        num_shots = sum(experiments[0].values())

        for experiment in experiments:
            if self.expected_state not in experiment:
                return 0
            else:
                current_probability = experiment[self.expected_state]/float(num_shots)
                if current_probability < minimal_probability:
                    minimal_probability = current_probability

        return minimal_probability


class AssertTeleported(AbstractAssertion):
    def __init__(self, qubit_to_teleport: Qubit, target_qubit: Qubit) -> None:
        self.qubit_to_teleport = qubit_to_teleport
        self.target_qubit = target_qubit

    def verify(self, experiments: List[Dict[str, int]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit_to_teleport not in resource_matcher or self.target_qubit not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(experiments)
        # TODO: this checks if prob check out but not if the qubit got teleported (maybe since -|0> != |0> but here they are)
        expected_ground_state_probability = resource_matcher[self.qubit_to_teleport].value.probabilities()[0]
        assert_probability = AssertProbability(self.target_qubit, 0, expected_ground_state_probability)
        return assert_probability.verify(experiments, resource_matcher)


class AssertTransformed(AbstractAssertion):
    def __init__(self, qubit: Qubit, phase_shift: float, angle_shift: float) -> None:  # TODO: is this naming even worth keeping, maybe just theta and phi will be more intuitive
        self.qubit = qubit
        self.phase_shift = phase_shift
        self.angle_shift = angle_shift

    def verify(self, experiments: List[Dict[str, int]], resource_matcher: Dict[Qubit, ConcreteQubit]) -> float:
        if self.qubit not in resource_matcher:
            raise NoQubitFoundError("qubit specified in the assertion is not specified in qubits property of the test")

        self.check_if_experiments_empty(experiments)
        # TODO: this checks if prob check out but not if the qubit got transformed (maybe since -|0> != |0> but here they are)

        qubit_initial_value = resource_matcher[self.qubit].value.to_dict()
        theta, phi = vector_state_to_hopf_coordinates(qubit_initial_value["0"], qubit_initial_value["1"])
        new_theta = theta + self.angle_shift
        new_phase = phi + self.phase_shift

        new_expected_state = Statevector(hopf_coordinates_to_vector_state(new_theta, new_phase))

        expected_ground_state_probability = new_expected_state.probabilities()[0]
        assert_probability = AssertProbability(self.qubit, 0, expected_ground_state_probability)
        return assert_probability.verify(experiments, resource_matcher)

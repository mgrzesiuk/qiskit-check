from scipy.spatial.transform import Rotation

from qiskit_check._test_engine.state_estimation.tomography_requirement import TomographyRequirement
from qiskit_check.property_test.assertions import AbstractAssertion, AssertStateEqual, AssertStateTransformed
from qiskit_check.property_test.assertions import AssertEqual, AssertTransformed
from qiskit_check.property_test.resources import AnyRange, Qubit
from qiskit_check.property_test.utils import amend_instruction_location


class TestTomographyRequirement:
    def test_required_tomography_returns_true_when_one_assertion_requires(self):
        assertions = [AssertStateEqual(Qubit(AnyRange()), 2, (0, 0))]
        tomography_requirement = TomographyRequirement(assertions)
        assert tomography_requirement.requires_tomography

    def test_required_tomography_returns_true_when_multiple_assertion_requires(self):
        q1 = Qubit(AnyRange())
        q2 = Qubit(AnyRange())
        assertions = [
            AssertStateEqual(q1, 2, (0, 0)),
            AssertEqual(q1, q2),
            AssertStateTransformed(q2, 4, Rotation.identity())
        ]
        tomography_requirement = TomographyRequirement(assertions)
        assert tomography_requirement.requires_tomography

    def test_required_tomography_returns_false_when_no_assertion_requires(self):
        q1 = Qubit(AnyRange())
        q2 = Qubit(AnyRange())
        assertions = [
            AssertEqual(q1, q2),
            AssertTransformed(q2, Rotation.identity())
        ]
        tomography_requirement = TomographyRequirement(assertions)
        assert not tomography_requirement.requires_tomography

    def test_qubits_requiring_tomography_stores_pairs_correctly_for_multiple_assertions(self):
        q1 = Qubit(AnyRange())
        q2 = Qubit(AnyRange())
        assertions = [
            AssertStateEqual(q1, 2, (0, 0)),
            AssertEqual(q1, q2),
            AssertStateTransformed(q2, 4, Rotation.identity()),
            AssertStateTransformed(q2, 6, Rotation.identity())
        ]
        tomography_requirement = TomographyRequirement(assertions)
        assert tomography_requirement.qubits_requiring_tomography[q1] == [amend_instruction_location(2)]
        assert tomography_requirement.qubits_requiring_tomography[q2] == [amend_instruction_location(4),
                                                                          amend_instruction_location(6)]

    def test_qubits_requiring_tomography_stores_pairs_correctly_for_one_assertions(self):
        q1 = Qubit(AnyRange())
        assertions = [
            AssertStateEqual(q1, 2, (0, 0)),
        ]
        tomography_requirement = TomographyRequirement(assertions)
        assert tomography_requirement.qubits_requiring_tomography[q1] == [amend_instruction_location(2)]

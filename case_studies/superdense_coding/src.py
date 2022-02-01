from qiskit import QuantumCircuit

"""
code from https://qiskit.org/textbook/ch-algorithms/superdense-coding.html
"""


def create_bell_pair(circuit: QuantumCircuit) -> QuantumCircuit:
    """
    Returns:
        QuantumCircuit: Circuit that produces a Bell pair
    """
    circuit.h(1)
    circuit.cx(1, 0)
    return circuit


def encode_message(circuit: QuantumCircuit, qubit: int, msg: str):
    """Encodes a two-bit message on qc using the superdense coding protocol
    Args:
        circuit (QuantumCircuit): Circuit to encode message on
        qubit (int): Which qubit to add the gate to
        msg (str): Two-bit message to send
    Returns:
        QuantumCircuit: Circuit that, when decoded, will produce msg
    Raises:
        ValueError if msg is wrong length or contains invalid characters
    """
    if len(msg) != 2 or not set(msg).issubset({"0", "1"}):
        raise ValueError(f"message '{msg}' is invalid")
    if msg[1] == "1":
        circuit.x(qubit)
    if msg[0] == "1":
        circuit.z(qubit)
    return circuit


def decode_message(circuit: QuantumCircuit) -> QuantumCircuit:
    circuit.cx(1, 0)
    circuit.h(1)
    return circuit


def superdense_coding(message: str) -> QuantumCircuit:
    circuit = QuantumCircuit(2)

    circuit = create_bell_pair(circuit)

    circuit = encode_message(circuit, 1, message)

    return decode_message(circuit)

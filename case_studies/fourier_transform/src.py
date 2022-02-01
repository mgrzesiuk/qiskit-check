import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile, Aer
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_histogram


def qft(num_qubits: int) -> QuantumCircuit:
    return QFT(num_qubits)


def inverse_qft(num_qubits: int) -> QuantumCircuit:
    return QFT(num_qubits, inverse=True)


def add_measurement(circuit: QuantumCircuit) -> QuantumCircuit:
    circuit.measure_all()
    return circuit


if __name__ == "__main__":
    qubit_number = 3
    qft_circuit = add_measurement(qft(qubit_number))
    qft_circuit.draw(output='mpl')
    backend = Aer.get_backend('aer_simulator')
    qft_circuit = transpile(qft_circuit, backend)

    result = backend.run(qft_circuit).result()

    plot_histogram(result.get_counts(), title='Bell-State counts')
    plt.show()

import matplotlib.pyplot as plt
from IPython.display import display

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, Aer, transpile
from qiskit.extensions import Initialize
from qiskit.quantum_info import random_statevector, Statevector
from qiskit.visualization import array_to_latex, plot_bloch_multivector

"""
code from https://qiskit.org/textbook/ch-algorithms/teleportation.html
"""


def quantum_teleportation() -> QuantumCircuit:
    qr = QuantumRegister(3, name="q")
    crz, crx = ClassicalRegister(1, name="crz"), ClassicalRegister(1, name="crx")
    circuit = QuantumCircuit(qr, crz, crx)

    # entangle
    circuit.h(1)
    circuit.cx(1, 2)

    circuit.cx(0, 1)
    circuit.h(0)

    circuit.measure(0, 0)
    circuit.measure(1, 1)

    circuit.x(2).c_if(crx, 1)  # Apply gates if the registers are in the state '1'
    circuit.z(2).c_if(crz, 1)

    return circuit


if __name__ == "__main__":
    psi = random_statevector(2)

    q_tele = quantum_teleportation(psi)
    q_tele.draw(output='mpl')

    backend = Aer.get_backend('aer_simulator')
    q_tele.save_statevector()

    result = backend.run(q_tele).result().get_statevector()

    plot_bloch_multivector(psi)
    plot_bloch_multivector(result)
    plt.show()

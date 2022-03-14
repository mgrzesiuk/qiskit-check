from qiskit_check._test_engine.state_estimation.cloning.abstract_cloner import AbstractCloner
from qiskit_check._test_engine.state_estimation.tomography.abstract_tomography import AbstractTomography


class StateEstimator:
    def __init__(self, cloner: AbstractCloner, tomography: AbstractTomography):
        pass

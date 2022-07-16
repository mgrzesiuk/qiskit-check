from abc import ABC
from math import pi
from typing import Dict, List, Tuple

from qiskit import QuantumCircuit
from qiskit.circuit import Instruction, Measure

from qiskit_check.property_test.assertions.abstract_assertion import AbstractAssertion


class AbstractDirectInversionStateAssertion(AbstractAssertion, ABC):
    @staticmethod
    def get_xyz_measurements() -> Tuple[Instruction]:
        return (AbstractDirectInversionStateAssertion.get_x_measurement(), AbstractDirectInversionStateAssertion.get_y_measurement(), AbstractDirectInversionStateAssertion.get_z_measurement())
    
    @staticmethod
    def get_x_measurement() -> Instruction:
        measure_name = "measure_x"
        qc = QuantumCircuit(1, 1,  name=measure_name)
        qc.h(0)
        qc.measure(0, 0)
        return qc.to_instruction(label=measure_name)
    
    @staticmethod
    def get_y_measurement() -> Instruction:
        measure_name = "measure_y"
        qc = QuantumCircuit(1, 1, name=measure_name)
        qc.rx(-pi/2, 0)
        qc.measure(0, 0)
        return qc.to_instruction(label=measure_name)
    
    @staticmethod
    def get_z_measurement() -> Instruction:
        return Measure()
    
    @staticmethod
    def combiner(experiments: List[List[Dict[str, int]]]) -> List[List[float]]:
        results = [[], [], []] #list of x coordinates, y coordinates, z coordinates for each test run
        for i in range(3):
            for experiment in experiments[i]:
                p = experiment["1"]/(experiment["0"] + experiment["1"])
                if i == 0: # x coordinate
                    results[i].append(1 - 2 * p)
                    continue                
                if i == 1: # y coordinate
                    results[i].append(2 * p - 1)
                    continue                
                if i == 2: # z coordinate:
                    results[i].append(1 - 2 * p)
                    continue
        return results
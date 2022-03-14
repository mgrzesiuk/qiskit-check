from qiskit_check._test_engine.generator.abstract_input_generator import QubitInputGeneratorFactory
from qiskit_check._test_engine.generator.abstract_input_generator import QubitInputGenerator


"""
https://math.stackexchange.com/questions/1304169/distance-between-two-points-on-a-sphere
"""
# TODO: add k-means ++ like generator (so probability based on distance from previous samples)
class NaivePPInputGenerator(QubitInputGenerator):
    pass


class NaivePPInputGeneratorFactory(QubitInputGeneratorFactory):
    pass

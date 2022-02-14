from qiskit_check._test_engine.collector import Collector
from qiskit_check._test_engine.generator.input_generator.uniform_input_generator import UniformInputGeneratorFactory
from qiskit_check._test_engine.printers.printer import TerminalPrinter
from qiskit_check._test_engine.processor import Processor
from qiskit_check._test_engine.test_runner.test_runner import SimulatorTestRunner
from qiskit_check._test_engine.assessor import AssessorFactory


def main():
    # TODO: figure out how to start code up properly
    test_collector = Collector()
    assessor_factory = AssessorFactory()
    qubit_input_generator_factory = UniformInputGeneratorFactory()
    test_runner = SimulatorTestRunner('aer_simulator')
    printer = TerminalPrinter()
    processor = Processor(test_collector, assessor_factory, qubit_input_generator_factory, test_runner, printer)
    processor.process(r"D:\coding\pytong\qiskit-sharp\case_studies")

from qiskit_check.test_engine.collector import Collector
from qiskit_check.test_engine.processor.processor import Processor


class CommandLineProcessor:
    """
    central part of the test engine, processor is a class responsible for putting together test collection, test
    generation and finally test running
    """
    def __init__(self, test_collector: Collector, processor: Processor) -> None:
        """
        initialize the processor
        Args:
            test_collector: Collector object to collect property test classes from given path
            qubits initial states
        """
        self.test_collector = test_collector
        self.processor = processor

    def process(self, root_test_directory: str) -> None:
        """
        collect property tests from a given directory or file and run them, returns exit code 0 if all tests passed,
        else returns exit code 1
        Args:
            root_test_directory: path to directory or file where the property tests are defined

        Returns: None

        """
        property_test_classes = self.test_collector.collect(root_test_directory)
        tests_succeeded, tests_failed = self.processor.process(property_test_classes)
        if len(tests_failed) > 0:
            exit(1)
        else:
            exit(0)
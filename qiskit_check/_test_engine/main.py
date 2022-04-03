from argparse import ArgumentParser, Namespace

from qiskit_check._test_engine.collector import Collector

from qiskit_check._test_engine.config import DefaultConfig, Config, AbstractConfig
from qiskit_check._test_engine.processor import Processor
from qiskit_check._test_engine.assessor import AssessorFactory


def get_argument_parser() -> ArgumentParser:
    arg_parser = ArgumentParser(description="property based testing of quantum circuits written in Qiskit")

    arg_parser.add_argument("-t", "--tests", type=str, required=True,
                            help="location of tests to run - directory or file")
    arg_parser.add_argument("-c", "--config", type=str, required=False, help="path to configuration .yaml file")
    return arg_parser


def get_configuration(args: Namespace) -> AbstractConfig:
    if args.config is None:
        return DefaultConfig()
    else:
        return Config(args.config)


def get_processor(configuration: AbstractConfig) -> Processor:
    test_collector = Collector()
    assessor_factory = AssessorFactory()

    qubit_input_generator_factory = configuration.get_input_generator_factory()
    runner = configuration.get_test_runner()

    return Processor(test_collector, assessor_factory, qubit_input_generator_factory, runner)


def main() -> None:
    arg_parser = get_argument_parser()
    args = arg_parser.parse_args()
    configuration = get_configuration(args)
    test_processor = get_processor(configuration)
    test_processor.process(args.tests)

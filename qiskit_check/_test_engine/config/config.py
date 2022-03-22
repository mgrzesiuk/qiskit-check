from yaml import safe_load

from qiskit_check._test_engine.config.default_config import DefaultConfig
from qiskit_check._test_engine.config.abstract_config import AbstractConfig
from qiskit_check._test_engine.generator import QubitInputGeneratorFactory
from qiskit_check._test_engine.test_runner import AbstractTestRunner
from qiskit_check._test_engine.utils import get_object_from_config


class Config(AbstractConfig):
    def __init__(self, config_path: str) -> None:
        self.config = safe_load(open(config_path))
        self.default_config = DefaultConfig()

    def get_test_runner(self) -> AbstractTestRunner:
        test_runner_key = "test_runner"
        if self.config is None or test_runner_key not in self.config:
            return self.default_config.get_test_runner()

        return get_object_from_config(self.config[test_runner_key])

    def get_input_generator_factory(self) -> QubitInputGeneratorFactory:
        input_generator_factory_key = "input_generator_factory"
        if self.config is None or input_generator_factory_key not in self.config:
            return self.default_config.get_input_generator_factory()

        return get_object_from_config(self.config[input_generator_factory_key])

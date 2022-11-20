import pytest
from pytest_mock import MockerFixture

from qiskit_check.test_engine.collector import Collector
from qiskit_check.test_engine.processor.command_line_processor import CommandLineProcessor
from qiskit_check.test_engine.processor.processor import Processor
from qiskit_check.test_engine.test_runner import AbstractTestRunner


class TestProcessor:
    def test_process_calls_correct_api_returns_0_when_correct_input_no_fails(self, mocker: MockerFixture):
        path = r"correct\path"
        collector_mock = mocker.patch.object(Collector, "collect")
        collector_mock.return_value = []

        assessor_factory_mock = mocker.MagicMock()
        qubit_input_generator_factory_mock = mocker.MagicMock()
        printer = mocker.MagicMock()

        test_runner_mock = mocker.patch.object(AbstractTestRunner, "run_tests")
        test_runner_mock.attach_mock(printer, "printer")
        test_runner_mock.run_tests.return_value = ([], [])

        processor = CommandLineProcessor(collector_mock,
                                         Processor(assessor_factory_mock,
                                                   qubit_input_generator_factory_mock, test_runner_mock))
        with pytest.raises(SystemExit) as exc:
            processor.process(path)

        assert exc.value.code == 0
        collector_mock.collect.assert_called_once_with(path)
        test_runner_mock.run_tests.assert_called_once_with(collector_mock.return_value)
        printer.print_summary.assert_called_once_with(*test_runner_mock.run_tests.return_value)

    def test_process_calls_correct_api_when_correct_exit_code_1_input_and_test_fails(self, mocker: MockerFixture):
        path = r"incorrect\path"
        collector_mock = mocker.patch.object(Collector, "collect")
        collector_mock.return_value = []

        assessor_factory_mock = mocker.MagicMock()
        qubit_input_generator_factory_mock = mocker.MagicMock()
        printer = mocker.MagicMock()

        test_runner_mock = mocker.patch.object(AbstractTestRunner, "run_tests")
        test_runner_mock.attach_mock(printer, "printer")
        test_runner_mock.run_tests.return_value = ([mocker.MagicMock()], [])

        processor = CommandLineProcessor(collector_mock,
                                         Processor(assessor_factory_mock,
                                                   qubit_input_generator_factory_mock, test_runner_mock))
        with pytest.raises(SystemExit) as exc:
            processor.process(path)
        assert exc.value.code == 1
        collector_mock.collect.assert_called_once_with(path)
        test_runner_mock.run_tests.assert_called_once_with(collector_mock.return_value)
        printer.print_summary.assert_called_once_with(*test_runner_mock.run_tests.return_value)

    def test_process_raises_exception_when_incorrect_path(self, mocker: MockerFixture):
        path = r"incorrect\path"
        collector_mock = mocker.patch.object(Collector, "collect")
        collector_mock.collect.side_effect = ValueError()

        assessor_factory_mock = mocker.MagicMock()
        qubit_input_generator_factory_mock = mocker.MagicMock()
        printer = mocker.MagicMock()

        test_runner_mock = mocker.patch.object(AbstractTestRunner, "run_tests")
        test_runner_mock.attach_mock(printer, "printer")
        test_runner_mock.run_tests.return_value = ([mocker.MagicMock()], [])

        processor = CommandLineProcessor(collector_mock, Processor(assessor_factory_mock,
                                                                   qubit_input_generator_factory_mock, test_runner_mock))
        with pytest.raises(ValueError):
            processor.process(path)

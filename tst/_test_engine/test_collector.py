import pytest
from pytest_mock import MockFixture

from qiskit_check._test_engine.collector import Collector


class TestCollector:
    def test_collect_error_raised_when_incorrect_path(self, mocker: MockFixture):
        mock_isfile = mocker.patch("os.path.isfile")
        mock_isfile.return_value = False
        mock_isdir = mocker.patch("os.path.isfile")
        mock_isdir.return_value = False
        collector = Collector()
        with pytest.raises(ValueError):
            collector.collect(r"correct\path")

    def test_collect_error_raised_when_non_python_file(self, mocker: MockFixture):
        mock_isfile = mocker.patch("os.path.isfile")
        mock_isfile.return_value = True
        mock_isdir = mocker.patch("os.path.isfile")
        mock_isdir.return_value = False
        collector = Collector()
        with pytest.raises(ValueError):
            collector.collect(r"correct\path\file")

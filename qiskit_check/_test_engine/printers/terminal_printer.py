from traceback import format_exception
from typing import List, Set, Type

from colorama import init, Fore, Style

from qiskit_check._test_engine.concrete_property_test.concerete_property_test import ConcretePropertyTest
from qiskit_check._test_engine.concrete_property_test.test_case import TestCase
from qiskit_check._test_engine.printers.abstract_printer import AbstractPrinter
from qiskit_check.property_test import PropertyTest


class TerminalPrinter(AbstractPrinter):
    def __init__(self) -> None:
        super().__init__()
        init(autoreset=True)

    def print_introduction(self, collected_tests: Set[Type[PropertyTest]]) -> None:
        print(f"{len(collected_tests)} tests found in the specified location, running them now.")

    def print_property_test_header(self, property_test: ConcretePropertyTest) -> None:
        print("starting property test: ", property_test.property_test_class.__name__)

    def print_test_case_header(self, test_case: TestCase) -> None:
        print("starting test with circuit:")
        print(test_case.circuit.draw(output="text"))

    def print_test_case_success(self, test_case: TestCase) -> None:
        print(f"test case {Fore.LIGHTGREEN_EX}passed")

    def print_test_case_failure(self, test_case: TestCase, error: Exception) -> None:
        print(f"test case {Fore.RED}FAILED{Style.RESET_ALL} with error:", error)
        print(Fore.RED + ''.join(format_exception(None, error, error.__traceback__)))

    def print_property_test_success(self, property_test: ConcretePropertyTest) -> None:
        print(f"entire property test {Fore.GREEN}PASSED")

    def print_property_test_failure(self, property_test: ConcretePropertyTest, error: Exception) -> None:
        print(f"entire property test {Fore.RED}FAILED{Style.RESET_ALL}", error)
        print(Fore.RED + ''.join(format_exception(None, error, error.__traceback__)))

    def print_summary(self, tests_failed: List[str], tests_succeeded: List[str]) -> None:
        print("all tests finished.")
        print(f"{len(tests_failed)} tests failed{':' if len(tests_failed) else '.'}")
        if len(tests_failed) > 0:
            for test in tests_failed:
                print(f"    {Fore.RED}{test}")
        print(f"{len(tests_succeeded)} tests succeeded{':' if len(tests_succeeded) else '.'}")
        if len(tests_succeeded) > 0:
            for test in tests_succeeded:
                print(f"    {Fore.GREEN}{test}")

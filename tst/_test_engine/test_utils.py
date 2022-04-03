import pytest

from qiskit_check._test_engine.utils import get_object_from_config


class DoubleNestedTestObject:
    def __init__(self, test_str: str, test_int: int):
        pass


class NestedTestObject:
    def __init__(self, double_nested_object: DoubleNestedTestObject, test_float: float):
        pass


class MainTestObject:
    def __init__(
            self, nested_object1: NestedTestObject, nested_object2: NestedTestObject,
            test_str: str, test_float: float, test_int: int):
        pass


class TestUtils:
    def test_get_object_from_config_creates_object_correctly_when_correct_dict_for_main(self):
        config = {
            "class": "tst._test_engine.test_utils.MainTestObject",
            "args": {
                "nested_object1": {
                    "class": "tst._test_engine.test_utils.NestedTestObject",
                    "args": {
                        "double_nested_object": {
                            "class": "tst._test_engine.test_utils.DoubleNestedTestObject",
                            "args": {
                                "test_str": "dasdas",
                                "test_int": 5
                            }
                        },
                        "test_float": 0.3,
                    }
                },
                "nested_object2": {
                    "class": "tst._test_engine.test_utils.NestedTestObject",
                    "args": {
                        "double_nested_object": {
                            "class": "tst._test_engine.test_utils.DoubleNestedTestObject",
                            "args": {
                                "test_str": "a23123",
                                "test_int": 9
                            }
                        },
                        "test_float": 0.4,
                    }
                },
                "test_str": "test",
                "test_float": 0.231,
                "test_int": 1
            }
        }

        obj = get_object_from_config(config)
        assert isinstance(obj, MainTestObject)

    def test_get_object_from_config_creates_object_correctly_when_correct_dict_for_nested(self):
        config = {
            "class": "tst._test_engine.test_utils.NestedTestObject",
            "args": {
                "double_nested_object": {
                    "class": "tst._test_engine.test_utils.DoubleNestedTestObject",
                    "args": {
                        "test_str": "dasdas",
                        "test_int": 5
                    }
                },
                "test_float": 0.3,
            }
        }
        obj = get_object_from_config(config)
        assert isinstance(obj, NestedTestObject)

    def test_get_object_from_config_error_raised_correctly_when_incorrect_dict_for_main(self):
        config = {
            "class": "tst._test_engine.test_utils.MainTestObject",
            "args": {
                "nested_object2": {
                    "class": "tst._test_engine.test_utils.NestedTestObject",
                    "args": {
                        "double_nested_object": {
                            "class": "tst._test_engine.test_utils.DoubleNestedTestObject",
                        },
                        "test_float": 0.4,
                    }
                },
                "test_str": "test",
                "test_float": 0.231,
                "test_int": 1
            }
        }

        with pytest.raises(TypeError):
            get_object_from_config(config)

    def test_get_object_from_config_error_raised_correctly_when_incorrect_dict_for_nested(self):
        config = {
            "class": "tst._test_engine.test_utils.NestedTestObject",
            "args": {
                "double_nested_object": {
                    "class": "tst._test_engine.test_utils.DoubleNestedTestObject",
                    "args": {
                        "test_str": "asd",
                        "test_int": -1
                    }
                }
            }
        }

        with pytest.raises(TypeError):
            get_object_from_config(config)

    def test_get_object_from_config_error_raised_correctly_when_incorrect_dict_for_nested_no_args(self):
        config = {
            "class": "tst._test_engine.test_utils.NestedTestObject",
        }

        with pytest.raises(TypeError):
            get_object_from_config(config)


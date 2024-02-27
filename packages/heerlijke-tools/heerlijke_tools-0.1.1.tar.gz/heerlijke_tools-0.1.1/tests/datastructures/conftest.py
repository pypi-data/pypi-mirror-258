from enum import auto

from heerlijke_tools.datastructures import CaseInsensitiveStrEnum


class EnumAuto(CaseInsensitiveStrEnum):
    FIRST = auto()
    SECOND = auto()
    THIRD = auto()


class EnumManual(CaseInsensitiveStrEnum):
    FIRST = "FIRST"
    SECOND = "SECOND"
    THIRD = "THIRD"


def pytest_generate_tests(metafunc):
    if 'input_enum' in metafunc.fixturenames:
        # Generate test cases based on the test_data list
        metafunc.parametrize(
            "input_enum",
            (EnumAuto, EnumManual),
            ids=("Auto", "Manual")
        )

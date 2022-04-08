import pytest

from sheet import LiteralCell


@pytest.mark.parametrize("literal_constant", [2, 4.5, "String"])
def test_init(literal_constant):
    LiteralCell(literal_constant)


@pytest.mark.parametrize(
    "literal_constant,expected_string", [[2, "2"], [4.5, "4.5"], ["String", "String"]]
)
def test_string_output(literal_constant, expected_string):
    cell = LiteralCell(literal_constant)
    assert cell.output.str == expected_string


@pytest.mark.parametrize(
    "literal_constant,expected_int", [[2, 2], [4.5, None], [-10, -10], ["String", None]]
)
def test_int_output(literal_constant, expected_int):
    cell = LiteralCell(literal_constant)
    assert cell.output.int == expected_int


@pytest.mark.parametrize(
    "literal_constant,expected_float",
    [[2, 2], [4.5, 4.5], [-10, -10], ["String", None]],
)
def test_float_output(literal_constant, expected_float):
    cell = LiteralCell(literal_constant)
    assert cell.output.float == expected_float

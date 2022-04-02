import pytest

from sheet import LiteralCell


@pytest.mark.parametrize("literal_constant", [2, 4.5, "String"])
@pytest.mark.xfail
def test_init(literal_constant):
    LiteralCell(literal_constant)


@pytest.mark.parametrize(
    "literal_constant,expected_string", [[2, "2"], [4.5, "4.5"], ["String", "String"]]
)
@pytest.mark.xfail
def test_string_output(literal_constant, expected_string):
    cell = LiteralCell(literal_constant)
    assert cell.output.string == expected_string


@pytest.mark.parametrize(
    "literal_constant,expected_int", [[2, 2], [4.5, None], [-10, -10], ["String", None]]
)
@pytest.mark.xfail
def test_int_output(literal_constant, expected_int):
    cell = LiteralCell(literal_constant)
    assert cell.output.int == expected_int

import pytest

from sheet import *


def test_init():
    CalculatedColumn()


@pytest.mark.xfail
def test_literal_as_formula():
    worksheet = Worksheet()
    column1 = Column()
    worksheet.add_columns(column1)
    column1[0] = CalculatedCell()
    column1[0].code = "1.1"
    assert column1[0].output.float == 1.1


@pytest.mark.xfail
def test_basic_no_relation():
    worksheet = Worksheet()
    column1 = Column()
    worksheet.add_columns(column1)
    column1[0] = CalculatedCell()
    column1[0].code = "1.1"
    column1[0].code = "random.randint(10,30)"
    assert 10 <= column1[0].output.float <= 30


@pytest.mark.xfail
def test_same_row_single_relation():
    worksheet = Worksheet()
    column1 = Column("Input")
    column2 = Column()
    worksheet.add_columns(column1, column2)
    column1[0] = LiteralCell(10)
    column2[0] = CalculatedCell()
    column2[0].code = ":Input + 1"
    assert column2[0].output.float == 11


@pytest.mark.xfail
def test_same_row_dependent_relations():
    worksheet = Worksheet()
    column1 = Column("Input")
    column2 = Column("FinalResult")
    column3 = Column("IntResult")
    worksheet.add_columns(column1, column2)
    column1[0] = LiteralCell(10)
    # Intentionally putting these in different order to what they must be
    # calculated
    column2[0] = CalculatedCell()
    column3[0] = CalculatedCell()
    column2[0].code = ":IntResult + 1"
    column3[0].code = ":Input / 2"
    assert column2[0].output.float == 6

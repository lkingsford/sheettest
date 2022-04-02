import pytest
from sheet import *


def test_init():
    Column()


@pytest.mark.xfail
def test_column_by_index():
    worksheet = Worksheet()
    column0 = Column()
    column1 = Column()
    worksheet.add_columns(column0, column1)
    assert worksheet.columns[0] == column0
    assert worksheet.columns[1] == column1


@pytest.mark.xfail
def test_column_by_label():
    worksheet = Worksheet()
    column0 = Column("Input")
    column1 = Column("Result")
    worksheet.add_columns(column0, column1)
    assert worksheet.columns["Input"] == column0
    assert worksheet.columns["Result"] == column1

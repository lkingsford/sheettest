import pytest

from sheet import *


def test_init():
    CalculatedColumn()


@pytest.mark.xfail
def test_literal_as_formula():
    worksheet = Worksheet()
    column1 = Column()
    column2 = CalculatedColumn()
    worksheet.add_columns(column1, column2)
    # Urgh. I don't know if this is what I want writing a new row to look like yet.
    column1[0] = LiteralCell("Test")
    column2.code = "1.1"
    assert column2[0].output.float == 1.1


@pytest.mark.xfail
def test_basic_no_relation():
    worksheet = Worksheet()
    column1 = Column()
    column2 = CalculatedColumn()
    worksheet.add_columns(column1, column2)
    column1[0] = LiteralCell("Test")
    # This code would require global imported as a module (which is, I think,
    # what I'll do for now)
    column2.code = "random.randint(10,30)"
    assert 10 <= column2[0].output.float <= 30


@pytest.mark.xfail
def test_same_row_single_relation():
    worksheet = Worksheet()
    column1 = Column("Input")
    column2 = CalculatedColumn()
    worksheet.add_columns(column1, column2)
    column1[0] = LiteralCell(10)
    # I don't know what format I like for references here yet
    # Part of me wants to make it explicit and separate
    column2.code = ":Input + 1"
    assert column2[0].output.float == 11


@pytest.mark.xfail
def test_same_row_dependent_relations():
    worksheet = Worksheet()
    column1 = Column("Input")
    column2 = CalculatedColumn("FinalResult")
    column3 = CalculatedColumn("IntResult")
    worksheet.add_columns(column1, column2, column3)
    column1[0] = LiteralCell(10)
    # Intentionally putting these in different order to what they must be
    # calculated
    column2.code = ":IntResult + 1"
    column3.code = ":Input / 2"
    assert column2[0].output.float == 6


@pytest.mark.xfail
def test_same_sheet_different_row():
    worksheet = Worksheet()
    column1 = Column("Input")
    column2 = CalculatedColumn("Result")
    worksheet.add_columns(column1, column2)
    for i in range(20):
        column1[i] = LiteralCell("Test")
    column2.code = ":Result[-1] + :Result[-2]"
    # Or maybe 'oor' for 'out of range', or maybe initial
    column2.default = "1"

    assert column2[0].output.float == 1
    assert column2[1].output.float == 1
    assert column2[2].output.float == 2
    assert column2[3].output.float == 3
    assert column2[4].output.float == 5
    assert column2[5].output.float == 8


@pytest.mark.xfail
def test_same_sheet_same_row_relative_reference():
    worksheet = Worksheet()
    column1 = Column("Input")
    column2 = CalculatedColumn("FinalResult")
    column3 = CalculatedColumn("IntResult")
    worksheet.add_columns(column1, column2)
    column1[0] = LiteralCell(10)
    # Not comfortable with this making row and column ambiguous
    # Compulsory comma? (like ':[1,]'?)
    column2.code = ":[1] + 1"
    column3.code = ":[-2] / 2"
    assert column2[0].output.float == 6


@pytest.mark.xfail
def test_difference_sheet():
    # TODO: Think about indexes between different sheets. Is treating the index
    # as the same a good idea!?
    workbook = Workbook()
    sheet1 = Worksheet("InputSheet")
    sheet2 = Worksheet("ResultSheet")
    workbook.add_sheets(sheet1, sheet2)
    sheet1.add_column(Column("Input"))
    sheet1.columns["Input"][0] = LiteralCell("25")
    sheet2.add_column(Column("Result"))
    sheet2.columns["Result"].code = ":InputSheet.Input / 2"
    assert sheet2.columns["Result"][0].output.float == 12.5


@pytest.mark.xfail
def test_absolute_reference():
    # TODO: This about how this would look
    worksheet = Worksheet()
    column1 = Column("Input")
    column2 = CalculatedColumn("Result")
    worksheet.add_columns(column1, column2)
    column1[0] = LiteralCell(10)
    column1[1] = LiteralCell(20)
    # Still not sure about this.
    # In theory, I think this should refer to cell 0,0 always.
    # Still not really comfortable. I want to think about indices more.
    column2.code = ":[&0,&0] + 1"
    assert column2[0].output.float == 11
    assert column2[1].output.float == 11


@pytest.mark.xfail
def test_dynamic_size_scale_no_ref():
    # Goal of this is to not expressly create a cell, or indicate the amount of
    # rows of the column, but still return
    worksheet = Worksheet()
    column1 = CalculatedColumn("Result")
    worksheet.add_columns(column1)
    column1.code = "10.1"
    # Should this require setting the column to 'lazy evaluate' or something?
    assert column1[10000].output.float == 10.1


@pytest.mark.xfail
def test_dynamic_size_different_row():
    worksheet = Worksheet()
    column1 = Column("Input")
    column2 = CalculatedColumn("Result")
    worksheet.add_columns(column1, column2)
    for i in range(20):
        column1[i] = LiteralCell("Test")
    column2.code = ":Result[-1] + :Result[-2]"
    column2.default = "1"

    # The 60th fibonacci number
    assert column2[59].output.float == 1548008755920

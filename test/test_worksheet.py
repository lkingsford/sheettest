import pytest

from sheet import *


def test_init():
    Worksheet()


@pytest.mark.xfail
def test_add_column():
    worksheet = Worksheet()
    column = Column("Test Column")
    worksheet.add_column(column)
    assert column in worksheet.columns


@pytest.mark.xfail
def test_remove_column():
    worksheet = Worksheet()
    column1 = Column()
    column2 = Column()
    column3 = Column()
    worksheet.add_column(column1)
    worksheet.add_column(column2)
    worksheet.add_column(column3)
    worksheet.remove_column(column2)
    assert column1 in worksheet.columns
    assert column2 not in worksheet.columns
    assert column3 in worksheet.columns


@pytest.mark.xfail
def test_add_column_correct_index():
    worksheet = Worksheet()
    column1 = Column()
    column2 = Column()
    worksheet.add_column(column1)
    worksheet.add_column(column2)
    assert column1.index == 0
    assert column2.index == 1


@pytest.mark.xfail
def test_append_data_from_list_rows():
    worksheet = Worksheet()
    headers = ["Artist", "Album", "Price"]
    values = [
        ["Courtney Barnett", "Tell me how you really feel", 41.84],
        ["Dream Theater", "The Astonishing", 88.02],
        ["Meat Loaf", "Bat out of Hell", 53.08],
    ]
    worksheet.append_from_rows(headers=headers, values=values)
    assert len(worksheet.columns.len) == 3
    for i, column in enumerate(worksheet.columns):
        assert column.label == headers[i]
    for i, row in enumerate(worksheet.rows):
        source_row = values[i]
        for j, cell in enumerate(row):
            source_data = source_row[j]
            if isinstance(source_data, str):
                assert cell.output.string == source_data
            else:
                assert cell.output.float == source_data


@pytest.mark.xfail
def test_append_data_from_dict_rows():
    worksheet = Worksheet()
    headers = ["Artist", "Album", "Price"]
    values = [
        {
            "Artist": "Courtney Barnett",
            "Album": "Tell me how you really feel",
            "Price": 41.84,
        },
        {"Artist": "Dream Theater", "Album": "The Astonishing", "Price": 88.02},
        {"Artist": "Meat Loaf", "Album": "Bat out of Hell", "Price": 53.08},
    ]
    worksheet.append_from_rows(values=values)
    assert len(worksheet.columns.len) == 3
    for i, column in enumerate(worksheet.columns):
        assert column.label == headers[i]
    for i, row in enumerate(worksheet.rows):
        source_row = values[i]
        # This relies on the dict being in the same order - which is not ideal
        # as a test
        for j, cell in enumerate(row):
            source_data = source_row.values()[j]
            if isinstance(source_data, str):
                assert cell.output.string == source_data
            else:
                assert cell.output.float == source_data


@pytest.mark.xfail
def test_expand_data_existing_worksheet_from_rows_no_index():
    worksheet = Worksheet()
    initial_headers = ["Artist", "Album", "Price"]
    initial_values = [
        ["Courtney Barnett", "Tell me how you really feel", 41.84],
        ["Dream Theater", "The Astonishing", 88.02],
        ["Meat Loaf", "Bat out of Hell", 53.08],
    ]
    worksheet.append_from_rows(headers=initial_headers, values=initial_values)

    new_headers = ["Sold", "Available"]
    new_values = [[6, 0], [4, 2], [3, 3]]
    worksheet.expand_from_rows(headers=new_headers, values=new_values)

    headers = initial_headers + new_headers
    assert len(worksheet.columns.len) == 3
    for i, column in enumerate(worksheet.columns):
        assert column.label == headers[i]
    for i, row in enumerate(worksheet.rows):
        source_row = initial_values[i] + new_values[i]
        for j, cell in enumerate(row):
            source_data = source_row[j]
            if isinstance(source_data, str):
                assert cell.output.string == source_data
            else:
                # This could be expanded to test the ints not as floats
                assert cell.output.float == source_data


@pytest.mark.xfail
def test_append_data_existing_worksheet_from_rows():
    worksheet = Worksheet()
    headers = ["Artist", "Album", "Price"]
    initial_values = [
        ["Courtney Barnett", "Tell me how you really feel", 41.84],
        ["Dream Theater", "The Astonishing", 88.02],
        ["Meat Loaf", "Bat out of Hell", 53.08],
    ]
    worksheet.append_from_rows(headers=headers, values=initial_values)

    new_values = [
        ["David Bowie", "Ziggy Stardust and the Spiders From Mars", 44.99],
        ["The Beatles", "Abbey Road (50th Anniversary Ed.)", 49.99],
    ]
    worksheet.expand_from_rows(headers=headers, values=new_values)

    assert len(worksheet.columns.len) == 3
    for i, column in enumerate(worksheet.columns):
        assert column.label == headers[i]
    for i, row in enumerate(worksheet.rows):
        source_row = initial_values[i] + new_values[i]
        for j, cell in enumerate(row):
            source_data = source_row[j]
            if isinstance(source_data, str):
                assert cell.output.string == source_data
            else:
                assert cell.output.float == source_data


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


@pytest.mark.xfail
def test_isolated_cell():
    worksheet = Worksheet()
    tax_rate_cell = LiteralCell("0.1")
    tax_rate_cell.label = "tax"
    # Or, add to cells? Dunno yet
    worksheet.add_cell(tax_rate_cell)
    column0 = Column("Price")
    column1 = CalculatedColumn("Total Price")
    column1.code = ":price + :price * :tax"
    column0[0] = LiteralCell("10")
    column0[1] = LiteralCell("20")
    worksheet.add_columns(column0, column1)

    assert column0[0].output.float == 11
    assert column0[1].output.float == 21

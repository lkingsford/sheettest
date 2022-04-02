import pytest

from sheet import Workbook
from sheet import Worksheet


def test_init():
    Workbook()


@pytest.mark.xfail
def test_add_worksheet():
    workbook = Workbook()
    worksheet = Worksheet()
    worksheet.add_sheet(worksheet)
    assert worksheet in workbook.sheets

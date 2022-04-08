"""A cell is a single value (calculated or literal) which may be in a column,
which may be in a sheet"""

from collections import namedtuple

from sheet.output import Output


class Cell:
    @property
    def output(self):
        return Output(None, None, None)

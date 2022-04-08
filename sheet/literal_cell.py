"""A cell containing a literal value"""

from enum import Enum
from typing import Union
from sheet.cell import Cell
from sheet.output import Output


class LiteralCell(Cell):
    class RawType(Enum):
        float = 0
        int = 1
        str = 2

    def __init__(self, value: Union[float, str, int]):
        self.raw_float = None
        self.raw_str = None
        self.raw_int = None
        if isinstance(value, int):
            self.raw_int = value
            self.raw_type = LiteralCell.RawType.int

        elif isinstance(value, float):
            self.raw_float = value
            self.raw_type = LiteralCell.RawType.float

        elif isinstance(value, str):
            self.raw_str = value
            self.raw_type = LiteralCell.RawType.str

    @property
    def output(self):
        # Should this be in
        if self.raw_type == LiteralCell.RawType.float:
            return Output(float=self.raw_float, str=str(self.raw_float), int=None)
        elif self.raw_type == LiteralCell.RawType.int:
            return Output(
                float=float(self.raw_int), str=str(self.raw_int), int=self.raw_int
            )

        return Output(float=None, str=self.raw_str, int=None)

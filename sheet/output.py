from dataclasses import dataclass, field


@dataclass
class Output:
    """Output of a cell"""

    float: float = field(repr=False, default=None)
    str: str = None
    int: int = field(repr=False, default=None)

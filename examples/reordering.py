"""Demonstrate ordering constraints (first/last/before/after)."""

from dataclasses import dataclass
from typing import Annotated

import bitstruct_annotated as ba


@dataclass
class Ordered:
    # Will end up first
    header: Annotated[int, ba.Unsigned(8, order="first")]
    # Placed right after header
    flag: Annotated[bool, ba.Bool(1, order="after:header")]
    # Padding to align next field on byte boundary
    _pad: Annotated[None, ba.PaddingZeros(7)]
    # Must appear before tail
    mid: Annotated[int, ba.Unsigned(16, order="before:tail")]
    # Last field
    tail: Annotated[int, ba.Unsigned(8, order="last")]


print("Format:", ba.format_string(Ordered))

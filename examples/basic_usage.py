"""Basic usage: define a dataclass with Annotated fields and pack/unpack it."""

from dataclasses import dataclass
from typing import Annotated

import bitstruct_annotated as ba


@dataclass
class Packet:
    # 8-bit unsigned integer
    version: Annotated[int, ba.Unsigned(8, order="first")]
    # 1 bit boolean
    flag: Annotated[bool, ba.Bool(1, order="after:version")]
    # 7 bits padding (to align next byte)
    _pad: Annotated[None, ba.PaddingZeros(7)]
    # 16-bit unsigned value
    value: Annotated[int, ba.Unsigned(16)]


p = Packet(1, True, None, 513)
raw = ba.pack(p)
print("Packed bytes:", raw)

# Prepare object to unpack into
p2 = Packet(0, False, None, 0)
ba.unpack(p2, raw)
print("Unpacked object:", p2)

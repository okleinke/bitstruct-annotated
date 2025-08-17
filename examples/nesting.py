"""Show nesting of structures using the Nested() marker."""
from dataclasses import dataclass
from typing import Annotated
import bitstruct_annotated as ba

@dataclass
class Inner:
    a: Annotated[int, ba.Unsigned(4)]
    b: Annotated[int, ba.Unsigned(8)]

@dataclass
class Outer:
    x: Annotated[int, ba.Unsigned(12, order="first")]
    inner: Annotated[Inner, ba.Nested()]
    y: Annotated[int, ba.Unsigned(16, order="last")]

instance = Outer(1, Inner(2, 3), 4)
print("Format string:", ba.format_string(Outer))
print("Values:", ba.field_values(instance))
print("Packed:", ba.pack(instance))

obj = Outer(0, Inner(0, 0), 0)
ba.unpack(obj, ba.pack(instance))
print("Unpacked:", obj)

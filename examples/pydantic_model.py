"""Use with a Pydantic BaseModel."""

from typing import Annotated

from pydantic import BaseModel, Field

import bitstruct_annotated as ba


class Car(BaseModel):
    make: Annotated[str, Field(max_length=32), ba.Text(32, order="first")]
    model: Annotated[str, Field(max_length=32), ba.Text(32, order="after:make")]
    year: Annotated[int, Field(ge=1900, le=2100), ba.Unsigned(16, order="last")]


c = Car(make="Toyo", model="Coro", year=2021)
print("Format string:", ba.format_string(Car))
print("Packed:", ba.pack(c))

c2 = Car(make="", model="", year=1900)
ba.unpack(c2, ba.pack(c))
print("Unpacked:", c2)

# bitstruct-annotated - Annotate fields with bitstruct un/packing instructions

This package provides metadata classes that can be used to annotate fields with
un/packing instructions for the [bitstruct](https://github.com/eerimoq/bitstruct)
package. In particular, this package is intended to be used in conjunction with
either [`dataclasses`](https://docs.python.org/3/library/dataclasses.html) or
Pydantic's [`BaseModel`](https://pydantic-docs.helpmanual.io/usage/models/).

Besides metadata classes for each format type supported by `bitstruct`, this
package also provides a metadata class to indicate nested structures.

Functions are provided to un/pack instances by calling `bitstruct` with the
format string, that is assembled from the metadata annotations.

## Installation

`bitstruct-annotated` can be installed from PyPI using pip:

```bash
pip install bitstruct-annotated
```

## Usage

The metadata classes provided by this package can be used in conjunction with
Python's built-in
[`Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated) 
type annotation:

```python
from dataclasses import dataclass
from typing import Annotated
import bitstruct_annotated as ba

@dataclass
class MyDataClass:
    other_field: int
    integer_field: Annotated[int, ba.Unsigned(size=8, msb_first=True)]
    padding_field: Annotated[int, ba.PaddingZeros(size=7, order='first')]
    boolean_field: Annotated[bool, ba.Bool(size=1, order='after:padding_field')]

mdc = MyDataClass(12, 34, 0, True)
packed = ba.pack(mdc)
# packed == b'\x01\x22'
```

In the example above, `Annotated` is used to include the un/packing
instructions as additional metadata in the field's type annotations. Fields
without annotation are ignored by the `bitstruct_annotated.pack` and
`bitstruct_annotated.unpack` functions.

While the `size` argument indicates the numbers of bits to be used for the field,
the `order` argument indicates the order in which the fields should be packed.
Here, the `padding_field` will be packed first, followed by the `boolean_field`.

The `msb_first` argument (default is `True`) can be set to `False` to reverse the
bit order of a field. Currently, the `bitstruct` package does not support alternate
byte orders. If required, the user has to swap bytes after packing by themselves.

The `bitstruct_annotated.format_string` function can be used to generate and
inspect the resulting bitstruct format string. To obtain values to be packed
from an instance, the `bitstruct_annotated.field_values` function can be used:

```python
# ... continued from the previous example
format_string = ba.format_string(MyDataClass)
# format_string == '>p7b1u8'
values = ba.field_values(mdc)
# values == (True, 34)
```

A similar example using Pydantic's `BaseModel`:

```python
from pydantic import BaseModel
from typing import Annotated
import bitstruct_annotated as ba

class MyPydanticModel(BaseModel):
    other_field: int
    integer_field: Annotated[int, ba.Unsigned(size=8, msb_first=True)]
    padding_field: Annotated[int, ba.PaddingZeros(size=7, order='first')]
    boolean_field: Annotated[bool, ba.Bool(size=1, order='after:padding_field')]


m = MyPydanticModel(other_field=0, integer_field=34, padding_field=0, boolean_field=True)
packed = ba.pack(m)
# packed == b'\x01\x22'
```

The following metadata classes are provided by this package:
- `Bool`: Boolean field.
- `Float`: To be used for floating-point field.
- `PaddingOnes`: A padding field filled with ones.
- `PaddingZeros`: A padding field filled with zeros.
- `Raw`: Contains raw data (bytes).
- `Signed`: Signed integer field.
- `Text`: Used for text fields (strings).
- `Unsigned`: Unsigned integer field.
- `Nested`: Nested structure - `bitstruct_annotated` will recurse into the
  field's type to look for additional annotations.

The following functions are provided by this package:
- `format_string`: Generate a bitstruct format string from a class.
- `field_values`: Extract values from an instance to be packed.
- `pack`: Pack an instance into a byte string.
- `unpack`: Unpack a byte string into an instance.

Note that the instance has to have been initialized first when unpacking.
This is necessary, because the `bitstruct_annotated.unpack` function does
not make any assumptions about the class' constructor.

For further information, refer to the docstrings of the functions and metadata
classes.

## Contributing

Currently, this project does not accept contributions.

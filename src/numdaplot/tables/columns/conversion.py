"""
A new type for a column of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.data_types.type import Type


@dataclass(frozen=True)
class Conversion:
	"""
	A new type for a column of a Table, used by ``Table.convert``.

	Accepted conversions: between number types, from numbers, booleans and categories to texts,
	from texts and categories to numbers or booleans, and from numbers, booleans and texts to categories.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The name of the column.
	dtype
		Its new type.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> codes = ndp.Table.from_arrays({"zip_code": ndp.Array.from_list(["06000", "75001"])})
	>>> codes.convert(ndp.Conversion(column="zip_code", dtype=ndp.Type.INT32))
	zip_code
	INT32
	0     6000
	1    75001
	"""

	column: str
	dtype: Type

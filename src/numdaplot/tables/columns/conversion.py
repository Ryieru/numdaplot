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
	>>> ndp.Conversion(column="zip_code", dtype=ndp.Type.TEXT)
	Conversion(column='zip_code', dtype=<Type.TEXT: 12>)
	"""

	column: str
	dtype: Type

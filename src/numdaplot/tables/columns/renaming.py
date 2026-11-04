"""
A new name for a column of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.tables.columns.column_names import require_column_name


@dataclass(frozen=True)
class Renaming:
	"""
	A new name for a column of a Table, used by ``Table.rename``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	old_name
		The current name of the column.
	new_name
		Its new name, a non-empty text.

	Raises
	------
	InvalidColumnNameError
		When ``new_name`` is empty.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.rename([ndp.Renaming(old_name="city", new_name="town")])
	    town   price
	    TEXT FLOAT64
	0  Paris   120.0
	1   Lyon    80.0
	2  Paris   150.0
	"""

	old_name: str
	new_name: str

	def __post_init__(self) -> None:
		"""
		Check that the new name is a non-empty text.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidColumnNameError
			When ``new_name`` is empty.
		"""
		require_column_name(self.new_name)

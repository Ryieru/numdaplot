"""
Settings of the removal of duplicated rows of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.settings.field_types import require_field_types
from numdaplot.tables.columns.column_names import copy_column_names
from numdaplot.tables.duplicates.keep import Keep


@dataclass(frozen=True)
class Deduplication:
	"""
	Which rows count as duplicates and which one is kept, used by ``Table.drop_duplicates``.

	Two missing values are equal when comparing rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	columns
		The names of the columns compared, every column when omitted.
		The deduplication keeps its own copy of the list.
	keep
		The row kept in each group of duplicates, the first one by default.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	EmptyListError
		When ``columns`` is an empty list.
	InvalidColumnNameError
		When a column name is an empty text.
	DuplicateColumnError
		When a column name appears twice.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.drop_duplicates(ndp.Deduplication(columns=["city"]))
	    city   price
	    TEXT FLOAT64
	0  Paris   120.0
	1   Lyon    80.0
	"""

	columns: list[str] | None = None
	keep: Keep = Keep.FIRST

	def __post_init__(self) -> None:
		"""
		Check the columns and replace them with a copy that only the deduplication holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		EmptyListError
			When ``columns`` is an empty list.
		InvalidColumnNameError
			When a column name is an empty text.
		DuplicateColumnError
			When a column name appears twice.
		"""
		require_field_types(self)

		if self.columns is None:
			return

		columns_copy = copy_column_names(self.columns)
		object.__setattr__(self, "columns", columns_copy)

"""
Settings of the sort of the rows of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.argument_checks.column_names import require_unique_names
from numdaplot.argument_checks.field_types import require_field_types
from numdaplot.errors.settings.empty_list_error import EmptyListError
from numdaplot.tables.sorting.sort_key import SortKey

SORT_KEY_ITEM_NAME = "sort key"


@dataclass(frozen=True)
class TableSorting:
	"""
	Columns the rows of a Table are sorted by, used by ``Table.sort``.

	Rows are sorted by the first key, then rows with the same value by the second key, and so on.
	Rows equal on every key keep their order.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Renamed from ``Sorting``.

	Parameters
	----------
	keys
		The sort keys, at least one, each on a different column. The sorting keeps its own copy of the list.

	Raises
	------
	InvalidTypeError
		When a setting is not of the type its annotation names.
	EmptyListError
		When ``keys`` is empty.
	DuplicateColumnError
		When two keys sort the same column.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> by_city = ndp.SortKey(column="city")
	>>> by_price = ndp.SortKey(column="price", order=ndp.Order.DESCENDING)
	>>> sales.sort(ndp.TableSorting(keys=[by_city, by_price]))
	    city   price
	    TEXT FLOAT64
	0   Lyon    80.0
	1  Paris   150.0
	2  Paris   120.0
	"""

	keys: list[SortKey]

	def __post_init__(self) -> None:
		"""
		Check the keys and replace them with a copy that only the sorting holds.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When a setting is not of the type its annotation names.
		EmptyListError
			When ``keys`` is empty.
		DuplicateColumnError
			When two keys sort the same column.
		"""
		require_field_types(self)

		if self.keys == []:
			raise EmptyListError(SORT_KEY_ITEM_NAME)

		key_columns = [key.column for key in self.keys]
		require_unique_names(key_columns)
		keys_copy = list(self.keys)
		object.__setattr__(self, "keys", keys_copy)

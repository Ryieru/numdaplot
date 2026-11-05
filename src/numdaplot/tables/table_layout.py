"""
Order and uniqueness of the rows of a Table.

.. versionadded:: 0.1.0
"""

from typing import Self

from numdaplot.tables.duplicates.deduplicated_frame import drop_duplicate_rows
from numdaplot.tables.duplicates.deduplication import Deduplication
from numdaplot.tables.sorting.sorted_frame import sort_frame
from numdaplot.tables.sorting.sorting import Sorting
from numdaplot.tables.table_data import TableData


class TableLayout(TableData):
	"""
	Order and uniqueness of the rows of a Table with ``sort`` and ``drop_duplicates``.

	.. versionadded:: 0.1.0
	"""

	def sort(self, sorting: Sorting) -> Self:
		"""
		Return the rows sorted by one or several columns.

		.. versionadded:: 0.1.0

		Parameters
		----------
		sorting
			The sort keys, each with its order and the place of its missing values.

		Returns
		-------
		Self
			A new Table, rows numbered from 0. Rows equal on every key keep their order.

		Raises
		------
		ColumnNotFoundError
			When a key names a column the Table does not have.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> table = ndp.Table.from_arrays({"price": ndp.Array.from_list([20.0, 10.0, 30.0])})
		>>> table.sort(ndp.Sorting(keys=[ndp.SortKey(column="price", order=ndp.Order.DESCENDING)]))
		    price
		  FLOAT64
		0    30.0
		1    20.0
		2    10.0
		"""
		sorted_frame = sort_frame(self._frame, sorting)
		sorted_table = self._wrap(sorted_frame)

		return sorted_table

	def drop_duplicates(self, deduplication: Deduplication | None = None) -> Self:
		"""
		Return the Table without its duplicated rows.

		.. versionadded:: 0.1.0

		Parameters
		----------
		deduplication
			The compared columns, every column when omitted, and the row kept in each group.
			Two missing values are equal.

		Returns
		-------
		Self
			A new Table, remaining rows in their order, numbered from 0.

		Raises
		------
		ColumnNotFoundError
			When a compared column does not exist.

		Examples
		--------
		>>> import numdaplot as ndp
		>>> table = ndp.Table.from_arrays({"city": ndp.Array.from_list(["Pau", "Lyon", "Pau"])})
		>>> table.drop_duplicates()
		   city
		   TEXT
		0   Pau
		1  Lyon
		"""
		if deduplication is None:
			deduplication = Deduplication()

		remaining_frame = drop_duplicate_rows(self._frame, deduplication)
		remaining_table = self._wrap(remaining_frame)

		return remaining_table

"""
Sort of the rows of a Table.

.. versionadded:: 0.1.0
"""

from typing import Literal

import pandas

from numdaplot.argument_checks.column_names import require_known_columns
from numdaplot.ordering.missing_position import MissingPosition
from numdaplot.ordering.order import Order
from numdaplot.tables.sorting.table_sorting import TableSorting

STABLE_SORT = "stable"
MISSING_PLACES = dict[MissingPosition, Literal["first", "last"]](
	{
		MissingPosition.FIRST: "first",
		MissingPosition.LAST: "last",
	}
)


def sort_frame(frame: pandas.DataFrame, sorting: TableSorting) -> pandas.DataFrame:
	"""
	Return the rows of a Table sorted by several columns, each with its own order and place of missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	sorting
		The sort keys.

	Returns
	-------
	pandas.DataFrame
		The sorted rows, numbered from 0. Rows equal on every key keep their order.

	Raises
	------
	ColumnNotFoundError
		When a key names a column the Table does not have.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.sorting.sorted_frame import sort_frame
	>>> frame = pandas.DataFrame({"city": ["Pau", "Lyon", "Pau"], "price": [1.0, 2.0, 3.0]})
	>>> by_city = ndp.SortKey(column="city")
	>>> by_price = ndp.SortKey(column="price", order=ndp.Order.DESCENDING)
	>>> sort_frame(frame, ndp.TableSorting(keys=[by_city, by_price]))
	   city  price
	0  Lyon    2.0
	1   Pau    3.0
	2   Pau    1.0
	"""
	column_names = [str(column_name) for column_name in frame.columns]
	key_columns = [key.column for key in sorting.keys]
	require_known_columns(key_columns, column_names)
	sorted_frame = frame
	reversed_keys = reversed(sorting.keys)

	# A stable sort by the last key first leaves the rows sorted by every key in order.
	for key in reversed_keys:
		is_ascending = key.order == Order.ASCENDING
		missing_place = MISSING_PLACES[key.missing]
		sorted_frame = sorted_frame.sort_values(
			by=key.column,
			ascending=is_ascending,
			na_position=missing_place,
			kind=STABLE_SORT,
		)

	numbered_frame = sorted_frame.reset_index(drop=True)

	return numbered_frame

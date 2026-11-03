"""
A column the rows of a Table are sorted by.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.ordering.missing_position import MissingPosition
from numdaplot.ordering.order import Order


@dataclass(frozen=True)
class SortKey:
	"""
	A column the rows of a Table are sorted by, used by ``Sorting``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The name of the column.
	order
		Ascending by default.
	missing
		Place of the missing values, last by default whatever the order.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> cities = ndp.Array.from_list(["Paris", "Lyon", "Paris"])
	>>> prices = ndp.Array.from_list([120.0, 80.0, 150.0])
	>>> sales = ndp.Table.from_arrays({"city": cities, "price": prices})
	>>> sales.sort(ndp.Sorting(keys=[ndp.SortKey(column="price", order=ndp.Order.DESCENDING)]))
	city   price
	TEXT FLOAT64
	0  Paris   150.0
	1  Paris   120.0
	2   Lyon    80.0
	"""

	column: str
	order: Order = Order.ASCENDING
	missing: MissingPosition = MissingPosition.LAST

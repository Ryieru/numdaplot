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
	>>> ndp.SortKey(column="price", order=ndp.Order.DESCENDING)
	SortKey(column='price', order=<Order.DESCENDING: 2>, missing=<MissingPosition.LAST: 2>)
	"""

	column: str
	order: Order = Order.ASCENDING
	missing: MissingPosition = MissingPosition.LAST

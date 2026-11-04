"""
Settings of the sort of an Array.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.ordering.missing_position import MissingPosition
from numdaplot.ordering.order import Order
from numdaplot.positions.axis import Axis


@dataclass(frozen=True)
class ArraySorting:
	"""
	Settings of the sort of an Array, used by ``Array.sort``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	order
		Ascending by default.
	axis
		``EACH_ROW`` sorts the values inside each row, ``EACH_COLUMN`` inside each column.
		An axis only applies to a two-dimensional Array. When omitted, each row is sorted,
		which sorts the whole Array when it has one dimension.
	missing
		Place of the missing values, last by default whatever the order.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> grid = ndp.Array.from_list([[3, 1], [2, 4]])
	>>> grid.sort(ndp.ArraySorting(order=ndp.Order.DESCENDING, axis=ndp.Axis.EACH_COLUMN))
	Array([[3, 4],
	       [2, 1]], dtype=INT64)
	"""

	order: Order = Order.ASCENDING
	axis: Axis | None = None
	missing: MissingPosition = MissingPosition.LAST

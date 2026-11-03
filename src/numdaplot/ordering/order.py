"""
Direction of a sort.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Order(Enum):
	"""
	Direction of a sort.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Order.DESCENDING
	<Order.DESCENDING: 2>
	"""

	ASCENDING = auto()
	"""From the smallest to the largest value. Default value."""

	DESCENDING = auto()
	"""From the largest to the smallest value."""

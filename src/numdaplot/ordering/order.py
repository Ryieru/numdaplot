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
	>>> prices = ndp.Array.from_list([20, 30, 10])
	>>> prices.sort(ndp.ArraySorting(order=ndp.Order.DESCENDING))
	Array([30, 20, 10], dtype=INT64)
	"""

	ASCENDING = auto()
	"""
	From the smallest to the largest value. Default value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([20, 30, 10])
	>>> prices.sort(ndp.ArraySorting(order=ndp.Order.ASCENDING))
	Array([10, 20, 30], dtype=INT64)
	"""

	DESCENDING = auto()
	"""
	From the largest to the smallest value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([20, 30, 10])
	>>> prices.sort(ndp.ArraySorting(order=ndp.Order.DESCENDING))
	Array([30, 20, 10], dtype=INT64)
	"""

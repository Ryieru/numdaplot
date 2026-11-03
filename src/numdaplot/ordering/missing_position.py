"""
Place of missing values in a sort.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class MissingPosition(Enum):
	"""
	Place of missing values in a sort, whatever the order.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([20.0, None, 10.0])
	>>> prices.sort(ndp.ArraySorting(missing=ndp.MissingPosition.FIRST))
	Array([nan, 10., 20.], dtype=FLOAT64)
	"""

	FIRST = auto()
	"""Missing values come before every other value."""

	LAST = auto()
	"""Missing values come after every other value, as in pandas. Default value."""

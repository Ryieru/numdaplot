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
	>>> ndp.MissingPosition.LAST
	<MissingPosition.LAST: 2>
	"""

	FIRST = auto()
	"""Missing values come before every other value."""

	LAST = auto()
	"""Missing values come after every other value, as in pandas. Default value."""

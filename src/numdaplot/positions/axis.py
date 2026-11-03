"""
Direction in which an operation runs on two-dimensional data.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Axis(Enum):
	"""
	Direction in which an operation runs on two-dimensional data.

	Each name describes the result: ``EACH_ROW`` handles every row on its own,
	so a statistic gives one value per row.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Axis.EACH_ROW
	<Axis.EACH_ROW: 1>
	"""

	EACH_ROW = auto()
	"""Every row is handled on its own: one result per row."""

	EACH_COLUMN = auto()
	"""Every column is handled on its own: one result per column."""

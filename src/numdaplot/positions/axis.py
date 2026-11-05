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

	Every method working along an axis takes it as its own ``axis`` argument, next to its settings:
	``Array.compute``, ``Array.sort``, ``Table.count_missing`` and ``Table.drop_missing``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> sales = ndp.Array.from_list([[1, 2], [3, 4]])
	>>> sales.compute(ndp.Sum(), axis=ndp.Axis.EACH_ROW)
	Array([3, 7], dtype=INT64)
	>>> sales.compute(ndp.Sum(), axis=ndp.Axis.EACH_COLUMN)
	Array([4, 6], dtype=INT64)
	"""

	EACH_ROW = auto()
	"""
	Every row is handled on its own: one result per row.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> sales = ndp.Array.from_list([[1, 2], [3, 4]])
	>>> sales.compute(ndp.Sum(), axis=ndp.Axis.EACH_ROW)
	Array([3, 7], dtype=INT64)
	"""

	EACH_COLUMN = auto()
	"""
	Every column is handled on its own: one result per column.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> sales = ndp.Array.from_list([[1, 2], [3, 4]])
	>>> sales.compute(ndp.Sum(), axis=ndp.Axis.EACH_COLUMN)
	Array([4, 6], dtype=INT64)
	"""

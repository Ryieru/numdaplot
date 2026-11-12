"""
How a ratio of missing values is compared with its threshold.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class RatioComparison(Enum):
	"""
	How a ratio of missing values is compared with its threshold, used by ``MissingRatio``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([120.0, None, 80.0, None])
	>>> stocks = ndp.Array.from_list([3.0, 5.0, None, 2.0])
	>>> table = ndp.Table.from_arrays({"price": prices, "stock": stocks})
	>>> half = ndp.MissingRatio(0.5, comparison=ndp.RatioComparison.ABOVE)
	>>> table.drop_missing(ndp.MissingDrop(rule=half), axis=ndp.Axis.EACH_COLUMN)
	    price   stock
	  FLOAT64 FLOAT64
	0   120.0     3.0
	1     NaN     5.0
	2    80.0     NaN
	3     NaN     2.0
	"""

	AT_LEAST = auto()
	"""
	The ratio reaches the threshold or goes beyond it. Default value.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([120.0, None, 80.0, None])
	>>> stocks = ndp.Array.from_list([3.0, 5.0, None, 2.0])
	>>> table = ndp.Table.from_arrays({"price": prices, "stock": stocks})
	>>> half = ndp.MissingRatio(0.5, comparison=ndp.RatioComparison.AT_LEAST)
	>>> table.drop_missing(ndp.MissingDrop(rule=half), axis=ndp.Axis.EACH_COLUMN)
	    stock
	  FLOAT64
	0     3.0
	1     5.0
	2     NaN
	3     2.0
	"""

	ABOVE = auto()
	"""
	The ratio goes beyond the threshold.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([120.0, None, 80.0, None])
	>>> stocks = ndp.Array.from_list([3.0, 5.0, None, 2.0])
	>>> table = ndp.Table.from_arrays({"price": prices, "stock": stocks})
	>>> half = ndp.MissingRatio(0.5, comparison=ndp.RatioComparison.ABOVE)
	>>> table.drop_missing(ndp.MissingDrop(rule=half), axis=ndp.Axis.EACH_COLUMN)
	    price   stock
	  FLOAT64 FLOAT64
	0   120.0     3.0
	1     NaN     5.0
	2    80.0     NaN
	3     NaN     2.0
	"""

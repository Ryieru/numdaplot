"""
How a quantity is measured: as a count or as a fraction of a whole.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class Measure(Enum):
	"""
	How a quantity is measured: as a count, or as a fraction of a whole between 0 and 1.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([12.5, None, 30.0, None])})
	>>> prices.count_missing(ndp.MissingCount(measure=ndp.Measure.COUNT)).to_value()
	2
	>>> prices.count_missing(ndp.MissingCount(measure=ndp.Measure.RATIO)).to_value()
	0.5
	"""

	COUNT = auto()
	"""
	A number of values. Default value.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([12.5, None, 30.0, None])})
	>>> prices.count_missing(ndp.MissingCount(measure=ndp.Measure.COUNT)).to_value()
	2
	"""

	RATIO = auto()
	"""
	A fraction of the values, between 0 and 1.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Table.from_arrays({"price": ndp.Array.from_list([12.5, None, 30.0, None])})
	>>> prices.count_missing(ndp.MissingCount(measure=ndp.Measure.RATIO)).to_value()
	0.5
	"""

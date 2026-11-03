"""
Arithmetic mean of the values statistic.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.statistics.statistic import Statistic


@dataclass(frozen=True)
class Mean(Statistic):
	"""
	Arithmetic mean of the values.

	Missing values are ignored.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([10.0, None, 30.0])
	>>> prices.compute(ndp.Mean()).to_value()
	20.0
	"""

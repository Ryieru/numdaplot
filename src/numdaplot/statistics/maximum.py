"""
Largest value statistic.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.statistics.statistic import Statistic


@dataclass(frozen=True)
class Max(Statistic):
	"""
	Largest value.

	Missing values are ignored.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.0, None, 30.0])
	>>> prices.compute(ndp.Max()).to_value()
	30.0
	"""

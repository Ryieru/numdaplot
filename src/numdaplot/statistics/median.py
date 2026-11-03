"""
Median of the values, the middle value once sorted statistic.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.statistics.statistic import Statistic


@dataclass(frozen=True)
class Median(Statistic):
	"""
	Median of the values, the middle value once sorted.

	It equals ``Quantile(0.5)``. Missing values are ignored.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> salaries = ndp.Array.from_list([1800, 2000, 9000])
	>>> salaries.compute(ndp.Median()).to_value()
	2000.0
	"""

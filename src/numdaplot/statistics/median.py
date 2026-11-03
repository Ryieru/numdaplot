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
	>>> ndp.Median()
	Median()
	"""

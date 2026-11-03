"""
Standard deviation statistic.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.statistics.statistic import Statistic


@dataclass(frozen=True)
class StandardDeviation(Statistic):
	"""
	Standard deviation of the values, how far they spread around the mean.

	``[10, 10, 10]`` gives 0, while ``[0, 10, 20]`` gives about 8.2. It is the population standard
	deviation, divided by the number of values as in numpy, not by that number minus one as in pandas.
	Missing values are ignored.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.StandardDeviation()
	StandardDeviation()
	"""

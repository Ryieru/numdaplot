"""
Number of distinct values that are not missing statistic.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.statistics.statistic import Statistic


@dataclass(frozen=True)
class CountDistinct(Statistic):
	"""
	Number of distinct values that are not missing.

	``[1, 1, 2]`` gives 2.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.CountDistinct()
	CountDistinct()
	"""

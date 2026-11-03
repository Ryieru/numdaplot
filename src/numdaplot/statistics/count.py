"""
Number of values that are not missing statistic.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.statistics.statistic import Statistic


@dataclass(frozen=True)
class Count(Statistic):
	"""
	Number of values that are not missing.

	Use ``count_missing`` to count the missing ones.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Count()
	Count()
	"""

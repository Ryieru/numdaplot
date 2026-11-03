"""
Number of times the most frequent value appears statistic.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.statistics.statistic import Statistic


@dataclass(frozen=True)
class MostFrequentCount(Statistic):
	"""
	Number of times the most frequent value appears.

	Works on any type, text included.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> sizes = ndp.Array.from_list(["M", "L", "M"])
	>>> sizes.compute(ndp.MostFrequentCount()).to_value()
	2
	"""

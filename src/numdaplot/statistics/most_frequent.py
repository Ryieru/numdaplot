"""
Value that appears the most often statistic.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.statistics.statistic import Statistic


@dataclass(frozen=True)
class MostFrequent(Statistic):
	"""
	Value that appears the most often.

	Works on any type, text included. Missing values are ignored.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> sizes = ndp.Array.from_list(["M", "L", "M"])
	>>> sizes.compute(ndp.MostFrequent()).to_value()
	'M'
	"""

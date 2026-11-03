"""
Sum of the values statistic.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.statistics.statistic import Statistic


@dataclass(frozen=True)
class Sum(Statistic):
	"""
	Sum of the values.

	Missing values are ignored.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> amounts = ndp.Array.from_list([10.5, None, 4.5])
	>>> amounts.compute(ndp.Sum()).to_value()
	15.0
	"""

"""
Each number read as a duration in a unit.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.dates.duration_unit import DurationUnit
from numdaplot.dates.time_function import TimeFunction


@dataclass(frozen=True)
class ToDuration(TimeFunction):
	"""
	Each number read as a duration in a unit: 1.5 in days gives 36 hours.

	The result is a ``DURATION`` Array, rounded to the nanosecond. Applies to integers and decimals, not to
	booleans. ``DurationIn`` does the opposite.

	.. versionadded:: 0.1.0

	Parameters
	----------
	unit
		The unit of the numbers.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> nights = ndp.Array.from_list([3, 10])
	>>> nights.apply(ndp.ToDuration(unit=ndp.DurationUnit.DAY))
	Array(['3 days 00:00:00', '10 days 00:00:00'], dtype=DURATION)
	"""

	unit: DurationUnit

"""
Each duration counted in a unit.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.dates.duration_unit import DurationUnit
from numdaplot.dates.time_function import TimeFunction


@dataclass(frozen=True)
class DurationIn(TimeFunction):
	"""
	Each duration counted in a unit, as a decimal number: 36 hours in days gives 1.5.

	The result is a ``FLOAT64`` Array. ``ToDuration`` does the opposite.

	.. versionadded:: 0.1.0

	Parameters
	----------
	unit
		The unit to count in.

	Examples
	--------
	>>> from datetime import date
	>>> import numdaplot as ndp
	>>> arrivals = ndp.Array.from_list([date(2026, 1, 1), date(2026, 1, 10)])
	>>> departures = ndp.Array.from_list([date(2026, 1, 4), date(2026, 1, 20)])
	>>> stays = departures - arrivals
	>>> stays.apply(ndp.DurationIn(unit=ndp.DurationUnit.DAY))
	Array([ 3., 10.], dtype=FLOAT64)
	"""

	unit: DurationUnit

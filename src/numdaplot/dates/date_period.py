"""
The period holding each date, such as its month.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.dates.period_unit import PeriodUnit
from numdaplot.dates.time_function import TimeFunction


@dataclass(frozen=True)
class DatePeriod(TimeFunction):
	"""
	The period holding each date or datetime, given by its first day: its month, its week...

	The result is a ``DATE`` Array, or a ``DATETIME`` Array for ``PeriodUnit.HOUR``. Add it to a Table with
	``add_column``, then name it in ``group_by`` to compute one result per period.

	.. versionadded:: 0.1.0

	Parameters
	----------
	unit
		The length of the periods. ``PeriodUnit.HOUR`` needs datetimes.

	Examples
	--------
	>>> from datetime import date
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([date(2026, 1, 5), date(2026, 1, 28), date(2027, 1, 9)])
	>>> days.apply(ndp.DatePeriod(unit=ndp.PeriodUnit.MONTH))
	Array(['2026-01-01', '2026-01-01', '2027-01-01'], dtype=DATE)
	"""

	unit: PeriodUnit

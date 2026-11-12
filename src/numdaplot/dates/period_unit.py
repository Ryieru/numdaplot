"""
Lengths of the periods DatePeriod groups dates by.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class PeriodUnit(Enum):
	"""
	Lengths of the periods ``DatePeriod`` groups dates by, such as the month or the week.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30)])
	>>> times.apply(ndp.DatePeriod(unit=ndp.PeriodUnit.MONTH))
	Array(['2026-12-01'], dtype=DATE)
	"""

	YEAR = auto()
	"""
	The year, starting on January 1.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30)])
	>>> times.apply(ndp.DatePeriod(unit=ndp.PeriodUnit.YEAR))
	Array(['2026-01-01'], dtype=DATE)
	"""

	QUARTER = auto()
	"""
	The quarter, starting on January 1, April 1, July 1 or October 1.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30)])
	>>> times.apply(ndp.DatePeriod(unit=ndp.PeriodUnit.QUARTER))
	Array(['2026-10-01'], dtype=DATE)
	"""

	MONTH = auto()
	"""
	The month, starting on its first day.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30)])
	>>> times.apply(ndp.DatePeriod(unit=ndp.PeriodUnit.MONTH))
	Array(['2026-12-01'], dtype=DATE)
	"""

	WEEK = auto()
	"""
	The week, starting on Monday.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30)])
	>>> times.apply(ndp.DatePeriod(unit=ndp.PeriodUnit.WEEK))
	Array(['2026-12-28'], dtype=DATE)
	"""

	DAY = auto()
	"""
	The day.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30)])
	>>> times.apply(ndp.DatePeriod(unit=ndp.PeriodUnit.DAY))
	Array(['2026-12-31'], dtype=DATE)
	"""

	HOUR = auto()
	"""
	The hour, starting at minute 0. Datetimes only, the result is a ``DATETIME``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30)])
	>>> times.apply(ndp.DatePeriod(unit=ndp.PeriodUnit.HOUR))
	Array(['2026-12-31 14:00:00'], dtype=DATETIME)
	"""

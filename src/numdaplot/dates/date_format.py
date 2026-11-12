"""
Common orders in which dates are written as texts.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class DateFormat(Enum):
	"""
	Common orders in which dates are written as texts, used by ``TableConversion``.

	When reading, the day, the month and the year are separated by ``"/"``, ``"-"`` or ``"."``, the same one twice;
	days and months may have one digit, years have four. A ``_TIME`` member also needs the time, as ``"14:30"``
	or ``"14:30:15"``, after a space, or after a ``"T"`` for ``YEAR_MONTH_DAY_TIME``. When writing, ``"/"`` separates
	the day-month and month-day orders and ``"-"`` the year-month-day order, and the time is written ``"14:30:15"``.

	Use ``CustomDateFormat`` for any other way of writing dates.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Table.from_arrays({"day": ndp.Array.from_list(["31/12/2026", "1.2.2026"])})
	>>> days.convert(ndp.TableConversion(column="day", dtype=ndp.Type.DATE, format=ndp.DateFormat.DAY_MONTH_YEAR))
	         day
	        DATE
	0 2026-12-31
	1 2026-02-01
	"""

	DAY_MONTH_YEAR = auto()
	"""
	The day, the month, then the year: ``"31/12/2026"``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Table.from_arrays({"day": ndp.Array.from_list(["31/12/2026"])})
	>>> days.convert(ndp.TableConversion(column="day", dtype=ndp.Type.DATE, format=ndp.DateFormat.DAY_MONTH_YEAR))
	         day
	        DATE
	0 2026-12-31
	"""

	MONTH_DAY_YEAR = auto()
	"""
	The month, the day, then the year: ``"12/31/2026"``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Table.from_arrays({"day": ndp.Array.from_list(["12/31/2026"])})
	>>> days.convert(ndp.TableConversion(column="day", dtype=ndp.Type.DATE, format=ndp.DateFormat.MONTH_DAY_YEAR))
	         day
	        DATE
	0 2026-12-31
	"""

	YEAR_MONTH_DAY = auto()
	"""
	The year, the month, then the day: ``"2026-12-31"``. Read by default when no format is given.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> days = ndp.Table.from_arrays({"day": ndp.Array.from_list(["2026-12-31"])})
	>>> days.convert(ndp.TableConversion(column="day", dtype=ndp.Type.DATE, format=ndp.DateFormat.YEAR_MONTH_DAY))
	         day
	        DATE
	0 2026-12-31
	"""

	DAY_MONTH_YEAR_TIME = auto()
	"""
	The day, the month, the year, then the time: ``"31/12/2026 14:30"``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> times = ndp.Table.from_arrays({"time": ndp.Array.from_list(["31/12/2026 14:30"])})
	>>> day_first = ndp.DateFormat.DAY_MONTH_YEAR_TIME
	>>> times.convert(ndp.TableConversion(column="time", dtype=ndp.Type.DATETIME, format=day_first))
	                 time
	             DATETIME
	0 2026-12-31 14:30:00
	"""

	MONTH_DAY_YEAR_TIME = auto()
	"""
	The month, the day, the year, then the time: ``"12/31/2026 14:30"``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> times = ndp.Table.from_arrays({"time": ndp.Array.from_list(["12/31/2026 14:30"])})
	>>> month_first = ndp.DateFormat.MONTH_DAY_YEAR_TIME
	>>> times.convert(ndp.TableConversion(column="time", dtype=ndp.Type.DATETIME, format=month_first))
	                 time
	             DATETIME
	0 2026-12-31 14:30:00
	"""

	YEAR_MONTH_DAY_TIME = auto()
	"""
	The year, the month, the day, then the time after a space or a ``"T"``: ``"2026-12-31 14:30"`` or
	``"2026-12-31T14:30"``.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> times = ndp.Table.from_arrays({"time": ndp.Array.from_list(["2026-12-31T14:30:15"])})
	>>> year_first = ndp.DateFormat.YEAR_MONTH_DAY_TIME
	>>> times.convert(ndp.TableConversion(column="time", dtype=ndp.Type.DATETIME, format=year_first))
	                 time
	             DATETIME
	0 2026-12-31 14:30:15
	"""

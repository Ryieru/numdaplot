"""
Parts of a date that DatePart reads.

.. versionadded:: 0.1.0
"""

from enum import Enum, auto


class DatePartUnit(Enum):
	"""
	Parts of a date that ``DatePart`` reads, such as its month or its day of the week.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30, 15)])
	>>> times.apply(ndp.DatePart(unit=ndp.DatePartUnit.MONTH))
	Array([12.], dtype=FLOAT64)
	"""

	YEAR = auto()
	"""
	The year, such as 2026.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30, 15)])
	>>> times.apply(ndp.DatePart(unit=ndp.DatePartUnit.YEAR))
	Array([2026.], dtype=FLOAT64)
	"""

	QUARTER = auto()
	"""
	The quarter of the year, from 1 for January to March to 4 for October to December.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30, 15)])
	>>> times.apply(ndp.DatePart(unit=ndp.DatePartUnit.QUARTER))
	Array([4.], dtype=FLOAT64)
	"""

	MONTH = auto()
	"""
	The month, from 1 for January to 12 for December.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30, 15)])
	>>> times.apply(ndp.DatePart(unit=ndp.DatePartUnit.MONTH))
	Array([12.], dtype=FLOAT64)
	"""

	WEEK = auto()
	"""
	The ISO week number, from 1 to 53. Week 1 holds the first Thursday of the year.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30, 15)])
	>>> times.apply(ndp.DatePart(unit=ndp.DatePartUnit.WEEK))
	Array([53.], dtype=FLOAT64)
	"""

	DAY = auto()
	"""
	The day of the month, from 1 to 31.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30, 15)])
	>>> times.apply(ndp.DatePart(unit=ndp.DatePartUnit.DAY))
	Array([31.], dtype=FLOAT64)
	"""

	WEEKDAY = auto()
	"""
	The day of the week, from 1 for Monday to 7 for Sunday.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30, 15)])
	>>> times.apply(ndp.DatePart(unit=ndp.DatePartUnit.WEEKDAY))
	Array([4.], dtype=FLOAT64)
	"""

	DAY_OF_YEAR = auto()
	"""
	The day of the year, from 1 to 366.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30, 15)])
	>>> times.apply(ndp.DatePart(unit=ndp.DatePartUnit.DAY_OF_YEAR))
	Array([365.], dtype=FLOAT64)
	"""

	HOUR = auto()
	"""
	The hour, from 0 to 23. Datetimes only.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30, 15)])
	>>> times.apply(ndp.DatePart(unit=ndp.DatePartUnit.HOUR))
	Array([14.], dtype=FLOAT64)
	"""

	MINUTE = auto()
	"""
	The minute, from 0 to 59. Datetimes only.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30, 15)])
	>>> times.apply(ndp.DatePart(unit=ndp.DatePartUnit.MINUTE))
	Array([30.], dtype=FLOAT64)
	"""

	SECOND = auto()
	"""
	The second, from 0 to 59. Datetimes only.

	Examples
	--------
	>>> from datetime import datetime
	>>> import numdaplot as ndp
	>>> times = ndp.Array.from_list([datetime(2026, 12, 31, 14, 30, 15)])
	>>> times.apply(ndp.DatePart(unit=ndp.DatePartUnit.SECOND))
	Array([15.], dtype=FLOAT64)
	"""

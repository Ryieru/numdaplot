"""
The range of dates, datetimes and durations that a count of nanoseconds holds.

.. versionadded:: 0.2.0
"""

from datetime import date, datetime, time, timedelta

LOWEST_DATETIME = datetime(1677, 9, 21, 0, 12, 43, 145225)
HIGHEST_DATETIME = datetime(2262, 4, 11, 23, 47, 16, 854775)
LONGEST_DURATION = timedelta(days=106751, seconds=85636, microseconds=854775)


def is_python_time_in_range(value: object) -> bool:
	"""
	Return whether a Python value is not a date, a datetime or a duration beyond a count of nanoseconds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		A single Python value.

	Returns
	-------
	bool
		False for a date, a datetime or a duration out of range, True for any other value.

	Examples
	--------
	>>> from datetime import datetime
	>>> from numdaplot.column_storage.time_range import is_python_time_in_range
	>>> is_python_time_in_range(datetime(2026, 1, 31))
	True
	>>> is_python_time_in_range(datetime(3000, 1, 31))
	False
	"""
	if isinstance(value, timedelta):
		duration_in_range = -LONGEST_DURATION <= value <= LONGEST_DURATION
		return duration_in_range

	if isinstance(value, datetime):
		clock_time = value.replace(tzinfo=None)
		datetime_in_range = LOWEST_DATETIME <= clock_time <= HIGHEST_DATETIME
		return datetime_in_range

	if isinstance(value, date):
		midnight = datetime.combine(value, time.min)
		date_in_range = LOWEST_DATETIME <= midnight <= HIGHEST_DATETIME
		return date_in_range

	return True

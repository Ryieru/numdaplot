"""
Date parts that cannot form a date, given to ValueConversionError.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RejectedDatePart:
	"""
	A part of a date that is not a whole number, such as the day 3.5.

	.. versionadded:: 0.1.0

	Parameters
	----------
	part_name
		``"year"``, ``"month"`` or ``"day"``.
	value
		The rejected number.

	Examples
	--------
	>>> from numdaplot.errors.rejected_dates import RejectedDatePart
	>>> RejectedDatePart("day", 3.5).value
	3.5
	"""

	part_name: str
	value: float


@dataclass(frozen=True)
class RejectedDate:
	"""
	A year, a month and a day that form no date, such as the 31st of February.

	.. versionadded:: 0.1.0

	Parameters
	----------
	year
		The year.
	month
		The month.
	day
		The day.

	Examples
	--------
	>>> from numdaplot.errors.rejected_dates import RejectedDate
	>>> RejectedDate(2025, 2, 31).day
	31
	"""

	year: int
	month: int
	day: int

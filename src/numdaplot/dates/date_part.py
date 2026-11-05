"""
A part of each date, such as its month.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.dates.date_part_unit import DatePartUnit
from numdaplot.dates.time_function import TimeFunction
from numdaplot.settings.field_types import require_field_types


@dataclass(frozen=True)
class DatePart(TimeFunction):
	"""
	A part of each date or datetime, as a number: its month, its day of the week...

	The result is a ``FLOAT64`` Array, so a missing date gives a missing part. Every January of every year
	gives 1: use ``DatePeriod`` to tell January 2026 from January 2027.

	.. versionadded:: 0.1.0

	Parameters
	----------
	unit
		The part to read. ``DatePartUnit.HOUR``, ``DatePartUnit.MINUTE`` and ``DatePartUnit.SECOND`` need datetimes.


	Raises
	------
	InvalidSettingTypeError
		When a setting is not of the type its annotation names.

	Examples
	--------
	>>> from datetime import date
	>>> import numdaplot as ndp
	>>> days = ndp.Array.from_list([date(2026, 1, 5), None, date(2027, 1, 9)])
	>>> days.apply(ndp.DatePart(unit=ndp.DatePartUnit.MONTH))
	Array([ 1., nan,  1.], dtype=FLOAT64)
	>>> days.apply(ndp.DatePart(unit=ndp.DatePartUnit.WEEKDAY))
	Array([ 1., nan,  6.], dtype=FLOAT64)
	"""

	unit: DatePartUnit

	def __post_init__(self) -> None:
		"""
		Check the type of every setting.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidSettingTypeError
			When a setting is not of the type its annotation names.
		"""
		require_field_types(self)

"""
A new type for a column of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.data_types.type import Type
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_format import DateFormat
from numdaplot.dates.time_zone_change import TimeZoneChange


@dataclass(frozen=True)
class Conversion:
	"""
	A new type for a column of a Table, used by ``Table.convert``.

	Accepted conversions: between number types, from numbers, booleans, categories, dates, datetimes and
	durations to texts, from texts and categories to numbers, booleans, dates or datetimes, from any type
	but categories to categories, and between dates and datetimes. A time zone change keeps the type
	``DATETIME``: give it alone, in a conversion of a datetime column to ``DATETIME``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		The name of the column.
	dtype
		Its new type.
	format
		How dates are written as texts, when texts are read as dates or datetimes, or dates or datetimes are
		written as texts. Texts are read as year, month and day separated by ``-`` when omitted, and
		written the same way, with the time for datetimes.
	timezone
		A change of the time zone of a datetime column.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> codes = ndp.Table.from_arrays({"zip_code": ndp.Array.from_list(["06000", "75001"])})
	>>> codes.convert(ndp.Conversion(column="zip_code", dtype=ndp.Type.INT32))
	  zip_code
	     INT32
	0     6000
	1    75001
	>>> days = ndp.Table.from_arrays({"day": ndp.Array.from_list(["31/12/2026"])})
	>>> days.convert(ndp.Conversion(column="day", dtype=ndp.Type.DATE, format=ndp.DateFormat.DAY_MONTH_YEAR))
	         day
	        DATE
	0 2026-12-31
	"""

	column: str
	dtype: Type
	format: DateFormat | CustomDateFormat | None = None
	timezone: TimeZoneChange | None = None

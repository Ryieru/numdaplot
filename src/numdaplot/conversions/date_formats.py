"""
What a date format holds, and how it is read and named.

.. versionadded:: 0.2.0
"""

from numdaplot.data_types.type import Type
from numdaplot.dates.custom_date_format import DATE_CODES, TIME_CODES, CustomDateFormat
from numdaplot.dates.date_format import DateFormat

DAY_FIRST = r"(?P<day>\d{1,2})(?P<separator>[/.-])(?P<month>\d{1,2})(?P=separator)(?P<year>\d{4})"
MONTH_FIRST = r"(?P<month>\d{1,2})(?P<separator>[/.-])(?P<day>\d{1,2})(?P=separator)(?P<year>\d{4})"
YEAR_FIRST = r"(?P<year>\d{4})(?P<separator>[/.-])(?P<month>\d{1,2})(?P=separator)(?P<day>\d{1,2})"
CLOCK = r"(?P<hour>\d{1,2}):(?P<minute>\d{2})(?::(?P<second>\d{2}))?"
WRITE_PATTERNS = {
	DateFormat.DAY_MONTH_YEAR: "%d/%m/%Y",
	DateFormat.MONTH_DAY_YEAR: "%m/%d/%Y",
	DateFormat.YEAR_MONTH_DAY: "%Y-%m-%d",
	DateFormat.DAY_MONTH_YEAR_TIME: "%d/%m/%Y %H:%M:%S",
	DateFormat.MONTH_DAY_YEAR_TIME: "%m/%d/%Y %H:%M:%S",
	DateFormat.YEAR_MONTH_DAY_TIME: "%Y-%m-%d %H:%M:%S",
}
TIME_FORMATS = frozenset(
	{DateFormat.DAY_MONTH_YEAR_TIME, DateFormat.MONTH_DAY_YEAR_TIME, DateFormat.YEAR_MONTH_DAY_TIME}
)
DEFAULT_FORMATS = {
	Type.DATE: DateFormat.YEAR_MONTH_DAY,
	Type.DATETIME: DateFormat.YEAR_MONTH_DAY_TIME,
}
READ_PATTERNS = {
	DateFormat.DAY_MONTH_YEAR: DAY_FIRST,
	DateFormat.MONTH_DAY_YEAR: MONTH_FIRST,
	DateFormat.YEAR_MONTH_DAY: YEAR_FIRST,
	DateFormat.DAY_MONTH_YEAR_TIME: DAY_FIRST + " " + CLOCK,
	DateFormat.MONTH_DAY_YEAR_TIME: MONTH_FIRST + " " + CLOCK,
	DateFormat.YEAR_MONTH_DAY_TIME: YEAR_FIRST + "[ T]" + CLOCK,
}
# Without a format, a datetime takes its time when it has one: to_csv leaves out a time of midnight on every row.
DEFAULT_READ_PATTERNS = {
	Type.DATE: YEAR_FIRST,
	Type.DATETIME: YEAR_FIRST + "(?:[ T]" + CLOCK + ")?",
}


def has_date(date_format: DateFormat | CustomDateFormat) -> bool:
	"""
	Return whether a format reads or writes a date: every common format does, and a pattern with a date code.

	.. versionadded:: 0.1.0

	Parameters
	----------
	date_format
		A common format or a custom pattern.

	Returns
	-------
	bool
		False only for a custom pattern of a time without date.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.date_formats import has_date
	>>> has_date(ndp.DateFormat.DAY_MONTH_YEAR), has_date(ndp.CustomDateFormat("%H:%M"))
	(True, False)
	"""
	if not isinstance(date_format, CustomDateFormat):
		return True

	pattern_has_date = any(date_code in date_format.pattern for date_code in DATE_CODES)

	return pattern_has_date


def has_time(date_format: DateFormat | CustomDateFormat) -> bool:
	"""
	Return whether a date format reads or writes a time.

	.. versionadded:: 0.1.0

	Parameters
	----------
	date_format
		A common format or a custom pattern.

	Returns
	-------
	bool
		True for the ``_TIME`` members of ``DateFormat``, and the patterns with an hour, minute, second or
		AM/PM code.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.date_formats import has_time
	>>> has_time(ndp.DateFormat.DAY_MONTH_YEAR)
	False
	"""
	if isinstance(date_format, CustomDateFormat):
		pattern_has_time = any(time_code in date_format.pattern for time_code in TIME_CODES)
		return pattern_has_time

	format_has_time = date_format in TIME_FORMATS

	return format_has_time


def find_read_format(target_type: Type, date_format: DateFormat | CustomDateFormat | None) -> str | CustomDateFormat:
	"""
	Return what texts are read with: a custom format, or the regular expression of a common or default format.

	.. versionadded:: 0.1.0

	Parameters
	----------
	target_type
		``DATE`` or ``DATETIME``, which sets how texts are read without a format.
	date_format
		How the texts are written, the default of the type when omitted.

	Returns
	-------
	str or CustomDateFormat
		The custom format, or the regular expression.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.date_formats import YEAR_FIRST, find_read_format
	>>> find_read_format(ndp.Type.DATE, None) == YEAR_FIRST
	True
	"""
	if isinstance(date_format, CustomDateFormat):
		return date_format

	if date_format is None:
		default_pattern = DEFAULT_READ_PATTERNS[target_type]
		return default_pattern

	common_pattern = READ_PATTERNS[date_format]

	return common_pattern


def find_format_name(target_type: Type, date_format: DateFormat | CustomDateFormat | None) -> str:
	"""
	Return how an error names the format texts were read with.

	.. versionadded:: 0.1.0

	Parameters
	----------
	target_type
		``DATE`` or ``DATETIME``, which sets the default format.
	date_format
		The format, the default of the type when omitted.

	Returns
	-------
	str
		The pattern of a custom format, or the name of the ``DateFormat`` member.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.date_formats import find_format_name
	>>> find_format_name(ndp.Type.DATETIME, None)
	'YEAR_MONTH_DAY_TIME'
	>>> find_format_name(ndp.Type.DATE, ndp.CustomDateFormat("%d %b %Y"))
	'%d %b %Y'
	"""
	if isinstance(date_format, CustomDateFormat):
		return date_format.pattern

	common_format = date_format
	if common_format is None:
		common_format = DEFAULT_FORMATS[target_type]

	return common_format.name

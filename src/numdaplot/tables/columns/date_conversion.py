"""
Conversion of Table columns between texts, dates, datetimes and durations.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pandas

from numdaplot.arrays.conversion.time_text import format_durations
from numdaplot.data_types.type import Type
from numdaplot.dates.custom_date_format import TIME_CODES, CustomDateFormat
from numdaplot.dates.date_format import DateFormat
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_missing, find_column_type
from numdaplot.tables.frames.frame_normalization import convert_to_type
from numdaplot.tables.frames.time_zones import find_column_time_zone

DAY_FIRST = r"(?P<day>\d{1,2})(?P<separator>[/.-])(?P<month>\d{1,2})(?P=separator)(?P<year>\d{4})"
MONTH_FIRST = r"(?P<month>\d{1,2})(?P<separator>[/.-])(?P<day>\d{1,2})(?P=separator)(?P<year>\d{4})"
YEAR_FIRST = r"(?P<year>\d{4})(?P<separator>[/.-])(?P<month>\d{1,2})(?P=separator)(?P<day>\d{1,2})"
CLOCK = r"(?P<hour>\d{1,2}):(?P<minute>\d{2})(?::(?P<second>\d{2}))?"
FULL_TEXT = "^{pattern}$"
READ_PATTERNS = {
	DateFormat.DAY_MONTH_YEAR: DAY_FIRST,
	DateFormat.MONTH_DAY_YEAR: MONTH_FIRST,
	DateFormat.YEAR_MONTH_DAY: YEAR_FIRST,
	DateFormat.DAY_MONTH_YEAR_TIME: DAY_FIRST + " " + CLOCK,
	DateFormat.MONTH_DAY_YEAR_TIME: MONTH_FIRST + " " + CLOCK,
	DateFormat.YEAR_MONTH_DAY_TIME: YEAR_FIRST + "[ T]" + CLOCK,
}
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
YEAR_PART = "year"
DATE_PARTS = [YEAR_PART, "month", "day", "hour", "minute", "second"]
NO_CLOCK_PART = "0"
# pandas carries an hour of 25 over to the next day, so impossible clock parts are refused first.
CLOCK_LIMITS = {"hour": 24, "minute": 60, "second": 60}
COLUMN_AXIS = "columns"
OFFSET_CODE = "%z"
COMPACT_OFFSET = r"([+-]\d{2})(\d{2})$"
SEPARATED_OFFSET = r"\1:\2"
NANOSECOND_DTYPE = "timedelta64[ns]"


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
	>>> from numdaplot.tables.columns.date_conversion import has_time
	>>> has_time(ndp.DateFormat.DAY_MONTH_YEAR)
	False
	"""
	if isinstance(date_format, CustomDateFormat):
		pattern_has_time = any(time_code in date_format.pattern for time_code in TIME_CODES)
		return pattern_has_time

	format_has_time = date_format in TIME_FORMATS

	return format_has_time


def parse_dates(column: Column, target_type: Type, date_format: DateFormat | CustomDateFormat) -> Column:
	"""
	Return a text column read as dates or datetimes.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A text or category column.
	target_type
		``DATE`` or ``DATETIME``.
	date_format
		How the texts are written. A format without time gives datetimes at midnight.

	Returns
	-------
	Column
		The dates or datetimes, missing texts staying missing.

	Raises
	------
	ValueConversionError
		At the first text that does not follow the format or is not a real date, such as ``"31/02/2026"``.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.date_conversion import parse_dates
	>>> texts = pandas.Series(["31/12/2026", None], dtype="string")
	>>> parse_dates(texts, ndp.Type.DATE, ndp.DateFormat.DAY_MONTH_YEAR).tolist()
	[Timestamp('2026-12-31 00:00:00'), NaT]
	"""
	source_type = find_column_type(column)
	text_column = convert_to_type(column, Type.TEXT)
	stripped_texts = text_column.str.strip()
	if isinstance(date_format, CustomDateFormat):
		moments = pandas.to_datetime(stripped_texts, format=date_format.pattern, errors="coerce")
	else:
		moments = read_common_format(stripped_texts, date_format)

	missing = find_column_missing(column)
	unread_moments = moments.isna()
	unread = unread_moments.to_numpy(dtype=numpy.bool_)
	rejected = unread & ~missing
	has_rejected = bool(rejected.any())
	if has_rejected:
		rejected_texts = text_column[rejected]
		first_rejected_text = rejected_texts.iloc[0]
		raise ValueConversionError(source_type.name, target_type.name, first_rejected_text)

	dates = convert_to_type(moments, target_type)

	return dates


def read_common_format(texts: Column, date_format: DateFormat) -> Column:
	"""
	Return texts read with a common date format, NaT where a text does not follow it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	texts
		A text column, without spaces around the texts.
	date_format
		The order of the day, the month and the year, and whether a time follows.

	Returns
	-------
	Column
		The datetimes, NaT for a missing text, a text that does not follow the format, or an impossible date
		or time such as ``"31/02/2026"`` or ``"25:00"``.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.date_conversion import read_common_format
	>>> texts = pandas.Series(["2026-12-31T14:30", "31/12/2026"], dtype="string")
	>>> read_common_format(texts, ndp.DateFormat.YEAR_MONTH_DAY_TIME).tolist()
	[Timestamp('2026-12-31 14:30:00'), NaT]
	"""
	read_pattern = READ_PATTERNS[date_format]
	full_pattern = FULL_TEXT.format(pattern=read_pattern)
	# Some versions of the pandas stubs leave the columns of the extracted parts unknown.
	extracted_parts = cast(Any, texts.str.extract(full_pattern))
	date_parts = extracted_parts.reindex(columns=DATE_PARTS, fill_value=NO_CLOCK_PART)
	filled_parts = date_parts.fillna(NO_CLOCK_PART)
	years = extracted_parts[YEAR_PART]
	has_date = years.notna()
	present_parts = filled_parts.where(has_date)
	number_parts = present_parts.astype(numpy.float64)
	clock_parts = number_parts[CLOCK_LIMITS.keys()]
	clock_limits = pandas.Series(CLOCK_LIMITS)
	out_of_range = clock_parts.ge(clock_limits)
	has_impossible_time = out_of_range.any(axis=COLUMN_AXIS)
	possible_parts = cast(pandas.DataFrame, number_parts.mask(has_impossible_time))
	moments = pandas.to_datetime(possible_parts, errors="coerce")

	return moments


def write_dates(column: Column, date_format: DateFormat | CustomDateFormat | None) -> Column:
	"""
	Return a date or datetime column written as texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A date or datetime column.
	date_format
		How to write the texts: year, month and day separated by ``"-"``, then the time for datetimes, when
		omitted. A datetime with a time zone is written with its offset, such as ``"+02:00"``, except with
		a custom pattern.

	Returns
	-------
	Column
		The texts, missing values staying missing.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.date_conversion import write_dates
	>>> days = pandas.Series(pandas.to_datetime(["2026-12-31", None])).astype("datetime64[s]")
	>>> write_dates(days, ndp.DateFormat.DAY_MONTH_YEAR).tolist()
	['31/12/2026', <NA>]
	"""
	source_type = find_column_type(column)
	chosen_format = DEFAULT_FORMATS[source_type]
	if date_format is not None:
		chosen_format = date_format

	if isinstance(chosen_format, CustomDateFormat):
		custom_texts = column.dt.strftime(chosen_format.pattern)
		custom_column = convert_to_type(custom_texts, Type.TEXT)
		return custom_column

	write_pattern = WRITE_PATTERNS[chosen_format]
	time_zone = find_column_time_zone(column)
	writes_offset = time_zone is not None and chosen_format in TIME_FORMATS
	if not writes_offset:
		plain_texts = column.dt.strftime(write_pattern)
		plain_column = convert_to_type(plain_texts, Type.TEXT)
		return plain_column

	offset_pattern = write_pattern + OFFSET_CODE
	compact_texts = column.dt.strftime(offset_pattern)
	offset_texts = compact_texts.str.replace(COMPACT_OFFSET, SEPARATED_OFFSET, regex=True)
	offset_column = convert_to_type(offset_texts, Type.TEXT)

	return offset_column


def write_durations(column: Column) -> Column:
	"""
	Return a duration column written as texts, as pandas writes durations.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A duration column.

	Returns
	-------
	Column
		Texts such as ``"1 days 12:00:00"``, missing values staying missing.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.columns.date_conversion import write_durations
	>>> write_durations(pandas.Series(pandas.to_timedelta(["36h", None]))).tolist()
	['1 days 12:00:00', <NA>]
	"""
	durations = column.to_numpy(dtype=NANOSECOND_DTYPE)
	duration_texts = format_durations(durations)
	# Some versions of the pandas stubs leave the type of a Series built from numpy texts unknown.
	text_column = cast(Any, pandas.Series(duration_texts))
	missing = find_column_missing(column)
	present_texts = text_column.mask(missing)
	texts = convert_to_type(present_texts, Type.TEXT)

	return texts


def convert_moments(column: Column, target_type: Type) -> Column:
	"""
	Return dates as datetimes at midnight, or datetimes as their dates.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A date or datetime column.
	target_type
		``DATE`` or ``DATETIME``.

	Returns
	-------
	Column
		The converted column. A datetime with a time zone gives the date of its clock time in that zone.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.date_conversion import convert_moments
	>>> times = pandas.Series(pandas.to_datetime(["2026-12-31 14:30"]))
	>>> convert_moments(times, ndp.Type.DATE).tolist()
	[Timestamp('2026-12-31 00:00:00')]
	"""
	if target_type == Type.DATETIME:
		datetimes = convert_to_type(column, Type.DATETIME)
		return datetimes

	clock_times = column
	time_zone = find_column_time_zone(column)
	if time_zone is not None:
		clock_times = column.dt.tz_localize(None)

	midnights = clock_times.dt.normalize()
	dates = convert_to_type(midnights, Type.DATE)

	return dates

"""
Writing of dates, datetimes and durations as texts, and conversion between dates and datetimes.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import pandas

from numdaplot.column_storage.column import Column
from numdaplot.column_storage.column_values import find_column_missing, find_column_type
from numdaplot.column_storage.frame_normalization import convert_to_type
from numdaplot.column_storage.time_text import format_durations
from numdaplot.column_storage.time_zones import find_column_time_zone
from numdaplot.conversions.date_formats import DEFAULT_FORMATS, TIME_FORMATS, WRITE_PATTERNS
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_format import DateFormat
from numdaplot.types.type import Type

OFFSET_CODE = "%z"
COMPACT_OFFSET = r"([+-]\d{2})(\d{2})$"
SEPARATED_OFFSET = r"\1:\2"
NANOSECOND_DTYPE = "timedelta64[ns]"


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
	>>> from numdaplot.conversions.date_conversion import write_dates
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
	>>> from numdaplot.conversions.date_conversion import write_durations
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
	>>> from numdaplot.conversions.date_conversion import convert_moments
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

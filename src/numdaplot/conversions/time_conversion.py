"""
Conversion of Table columns to and from times of day.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pandas

from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_missing, find_column_type
from numdaplot.tables.frames.frame_normalization import convert_to_type
from numdaplot.tables.frames.time_columns import write_time_texts_column
from numdaplot.tables.frames.time_zones import find_column_time_zone
from numdaplot.types.time_of_day import TIME_DTYPE
from numdaplot.types.type import Type

DEFAULT_TIME_FORMAT_NAME = "HH:MM:SS"
CLOCK_PATTERN = r"^(?P<hour>\d{1,2}):(?P<minute>\d{2})(?::(?P<second>\d{2})(?:\.(?P<fraction>\d{1,6}))?)?$"
CLOCK_PARTS = ["hour", "minute", "second"]
CLOCK_LIMITS = {"hour": 24, "minute": 60, "second": 60}
FRACTION_PART = "fraction"
FRACTION_DIGITS = 6
FRACTION_PADDING = "0"
MISSING_PART = "0"
MICROSECONDS_PER_UNIT = {"hour": 3_600_000_000, "minute": 60_000_000, "second": 1_000_000}
COLUMN_AXIS = "columns"
REFERENCE_DAY = pandas.Timestamp("1900-01-01")
MICROSECOND_UNIT = "us"


def parse_times(column: Column, time_format: CustomDateFormat | None) -> Column:
	"""
	Return a text or category column read as times of day.

	The spaces around each text are removed. Without format, ``HH:MM``, ``HH:MM:SS`` and ``HH:MM:SS.ffffff`` are
	read, the hour having one or two digits.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A text or category column.
	time_format
		A pattern of a time without date, such as ``"%H%M"``, or None for the default reading.

	Returns
	-------
	Column
		A ``TIME`` column, missing values staying missing.

	Raises
	------
	ValueConversionError
		At the first text that is not a time in the format.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.time_conversion import parse_times
	>>> parse_times(pandas.Series(["15:35", " 8:05:30.5", None], dtype="string"), None).tolist()
	[Timedelta('0 days 15:35:00'), Timedelta('0 days 08:05:30.500000'), NaT]
	>>> parse_times(pandas.Series(["1535"], dtype="string"), ndp.CustomDateFormat("%H%M")).tolist()
	[Timedelta('0 days 15:35:00')]
	"""
	source_type = find_column_type(column)
	text_column = convert_to_type(column, Type.TEXT)
	stripped_texts = text_column.str.strip()
	times = read_times(stripped_texts, time_format)
	missing = find_column_missing(column)
	unread_times = times.isna()
	unread = unread_times.to_numpy(dtype=numpy.bool_)
	rejected = unread & ~missing
	has_rejected = bool(rejected.any())
	if has_rejected:
		rejected_texts = text_column[rejected]
		first_rejected_text = rejected_texts.iloc[0]
		format_name = find_time_format_name(time_format)
		raise ValueConversionError(source_type.name, Type.TIME.name, first_rejected_text, format_name)

	return times


def read_times(texts: Column, time_format: CustomDateFormat | None) -> Column:
	"""
	Return texts read as times of day, NaT where a text is not a time in the format.

	.. versionadded:: 0.1.0

	Parameters
	----------
	texts
		A column of texts without spaces around them.
	time_format
		A pattern of a time without date, or None for the default reading.

	Returns
	-------
	Column
		A column in ``timedelta64[us]``.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.conversions.time_conversion import read_times
	>>> read_times(pandas.Series(["24:00", "23:59"], dtype="string"), None).tolist()
	[NaT, Timedelta('0 days 23:59:00')]
	"""
	if time_format is None:
		default_times = read_clock_texts(texts)
		return default_times

	moments = pandas.to_datetime(texts, format=time_format.pattern, errors="coerce")
	moment_column = cast(Column, moments)
	custom_times = keep_time_of_day(moment_column)

	return custom_times


def read_clock_texts(texts: Column) -> Column:
	"""
	Return texts written as ``HH:MM``, ``HH:MM:SS`` or ``HH:MM:SS.ffffff`` read as times of day.

	.. versionadded:: 0.1.0

	Parameters
	----------
	texts
		A column of texts without spaces around them.

	Returns
	-------
	Column
		A column in ``timedelta64[us]``, NaT where a text is not such a time, or has an hour from 24, a minute or a
		second from 60.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.conversions.time_conversion import read_clock_texts
	>>> read_clock_texts(pandas.Series(["9:07", "12:60", "noon"], dtype="string")).tolist()
	[Timedelta('0 days 09:07:00'), NaT, NaT]
	"""
	# Some versions of the pandas stubs leave the columns of the extracted parts unknown.
	extracted_parts = cast(Any, texts.str.extract(CLOCK_PATTERN))
	hours = extracted_parts[CLOCK_PARTS[0]]
	is_clock = hours.notna()
	clock_parts = extracted_parts[CLOCK_PARTS].fillna(MISSING_PART)
	number_parts = clock_parts.where(is_clock).astype(numpy.float64)
	clock_limits = pandas.Series(CLOCK_LIMITS)
	out_of_range = number_parts.ge(clock_limits)
	is_impossible = out_of_range.any(axis=COLUMN_AXIS)
	microsecond_weights = pandas.Series(MICROSECONDS_PER_UNIT)
	weighted_parts = number_parts.mul(microsecond_weights)
	whole_microseconds = weighted_parts.sum(axis=COLUMN_AXIS, min_count=len(CLOCK_PARTS))
	fractions = read_fraction_microseconds(extracted_parts[FRACTION_PART])
	microseconds = whole_microseconds + fractions
	possible_microseconds = microseconds.mask(is_impossible)
	# Some versions of the pandas stubs leave the types of to_timedelta, fillna and mask partly unknown.
	time_pandas = cast(Any, pandas)
	raw_times = time_pandas.to_timedelta(possible_microseconds, unit=MICROSECOND_UNIT)
	times = cast(Column, raw_times)
	time_column = times.astype(TIME_DTYPE)

	return time_column


def read_fraction_microseconds(fractions: Column) -> Column:
	"""
	Return the decimal part of seconds, written with 1 to 6 digits, as microseconds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	fractions
		The digits after the decimal point, missing when there are none.

	Returns
	-------
	Column
		The microseconds, 0 where there are no digits.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.conversions.time_conversion import read_fraction_microseconds
	>>> read_fraction_microseconds(pandas.Series(["5", "000250", None], dtype=object)).tolist()
	[500000.0, 250.0, 0.0]
	"""
	# Some versions of the pandas stubs leave the types of fillna partly unknown.
	fraction_column = cast(Any, fractions)
	filled_fractions = cast(Column, fraction_column.fillna(MISSING_PART))
	text_fractions = filled_fractions.astype(str)
	padded_fractions = text_fractions.str.ljust(FRACTION_DIGITS, FRACTION_PADDING)
	microseconds = padded_fractions.astype(numpy.float64)

	return microseconds


def keep_time_of_day(moments: Column) -> Column:
	"""
	Return the time of day of datetimes, the local time for datetimes with a time zone.

	.. versionadded:: 0.1.0

	Parameters
	----------
	moments
		A column of datetimes, NaT where missing.

	Returns
	-------
	Column
		A column in ``timedelta64[us]``: the time since the midnight of each day.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.conversions.time_conversion import keep_time_of_day
	>>> keep_time_of_day(pandas.Series(pandas.to_datetime(["2026-03-14 15:35"]))).tolist()
	[Timedelta('0 days 15:35:00')]
	"""
	local_moments = moments
	time_zone = find_column_time_zone(moments)
	if time_zone is not None:
		local_moments = moments.dt.tz_localize(None)

	midnights = local_moments.dt.normalize()
	since_midnight = local_moments - midnights
	times = since_midnight.astype(TIME_DTYPE)

	return times


def write_times(column: Column, time_format: CustomDateFormat | None) -> Column:
	"""
	Return a column of times of day written as texts.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A ``TIME`` column.
	time_format
		A pattern of a time without date, such as ``"%Hh%M"``, or None for ``15:35:00``, with microseconds only
		when there are some.

	Returns
	-------
	Column
		A ``TEXT`` column, missing values staying missing.

	Examples
	--------
	>>> import numpy
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.time_conversion import write_times
	>>> times = pandas.Series(numpy.array([56100000000, "NaT"], dtype="timedelta64[us]"))
	>>> write_times(times, None).tolist()
	['15:35:00', <NA>]
	>>> write_times(times, ndp.CustomDateFormat("%Hh%M")).tolist()
	['15h35', <NA>]
	"""
	missing = column.isna()
	if time_format is None:
		# Some versions of the pandas stubs leave the types of mask partly unknown.
		default_texts = cast(Any, write_time_texts_column(column))
		present_texts = cast(Column, default_texts.mask(missing))
		default_column = convert_to_type(present_texts, Type.TEXT)
		return default_column

	moments = REFERENCE_DAY + column
	custom_texts = moments.dt.strftime(time_format.pattern)
	custom_column = convert_to_type(custom_texts, Type.TEXT)

	return custom_column


def find_time_format_name(time_format: CustomDateFormat | None) -> str:
	"""
	Return the name of the format times of day are read with.

	.. versionadded:: 0.1.0

	Parameters
	----------
	time_format
		A pattern of a time without date, or None for the default reading.

	Returns
	-------
	str
		The pattern, or ``HH:MM:SS`` for the default reading.

	Examples
	--------
	>>> from numdaplot.conversions.time_conversion import find_time_format_name
	>>> find_time_format_name(None)
	'HH:MM:SS'
	"""
	if time_format is None:
		return DEFAULT_TIME_FORMAT_NAME

	return time_format.pattern

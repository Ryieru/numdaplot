"""
Reading of texts as dates and datetimes, with a date format or without.

.. versionadded:: 0.2.0
"""

from typing import Any, cast

import numpy
import pandas

from numdaplot.conversions.date_formats import DEFAULT_READ_PATTERNS, READ_PATTERNS, find_format_name, find_read_format
from numdaplot.conversions.date_range import is_text_out_of_range
from numdaplot.data_types.type import Type
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_format import DateFormat
from numdaplot.errors.time_overflow_error import TimeOverflowError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_missing, find_column_type
from numdaplot.tables.frames.frame_normalization import convert_to_type

FULL_TEXT = "^{pattern}$"
YEAR_PART = "year"
DATE_PARTS = [YEAR_PART, "month", "day", "hour", "minute", "second"]
NO_CLOCK_PART = "0"
# pandas carries an hour of 25 over to the next day, so impossible clock parts are refused first.
CLOCK_LIMITS = {"hour": 24, "minute": 60, "second": 60}
COLUMN_AXIS = "columns"
CONVERT_OPERATION = "convert"


def parse_dates(column: Column, target_type: Type, date_format: DateFormat | CustomDateFormat | None) -> Column:
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
		How the texts are written. A format without time gives datetimes at midnight. When omitted, texts are read
		as year, month and day, and for datetimes each text may also have a time.

	Returns
	-------
	Column
		The dates or datetimes, missing texts staying missing.

	Raises
	------
	ValueConversionError
		At the first text that does not follow the format or is not a real date, such as ``"31/02/2026"``.
	TimeOverflowError
		When the version of pandas in use reads no date for a text holding a real date out of range.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.date_reading import parse_dates
	>>> texts = pandas.Series(["31/12/2026", None], dtype="string")
	>>> parse_dates(texts, ndp.Type.DATE, ndp.DateFormat.DAY_MONTH_YEAR).tolist()
	[Timestamp('2026-12-31 00:00:00'), NaT]
	>>> times = pandas.Series(["2026-12-31", "2026-12-31 14:30"], dtype="string")
	>>> parse_dates(times, ndp.Type.DATETIME, None).tolist()
	[Timestamp('2026-12-31 00:00:00'), Timestamp('2026-12-31 14:30:00')]
	"""
	source_type = find_column_type(column)
	text_column = convert_to_type(column, Type.TEXT)
	stripped_texts = text_column.str.strip()
	moments = read_moments(stripped_texts, target_type, date_format)
	missing = find_column_missing(column)
	unread_moments = moments.isna()
	unread = unread_moments.to_numpy(dtype=numpy.bool_)
	rejected = unread & ~missing
	has_rejected = bool(rejected.any())
	if has_rejected:
		rejected_texts = text_column[rejected]
		first_rejected_text = rejected_texts.iloc[0]
		read_format = find_read_format(target_type, date_format)
		is_out_of_range = is_text_out_of_range(first_rejected_text, read_format)
		if is_out_of_range:
			raise TimeOverflowError(CONVERT_OPERATION, target_type.name)

		format_name = find_format_name(target_type, date_format)
		raise ValueConversionError(source_type.name, target_type.name, first_rejected_text, format_name)

	dates = convert_to_type(moments, target_type)

	return dates


def read_moments(texts: Column, target_type: Type, date_format: DateFormat | CustomDateFormat | None) -> Column:
	"""
	Return texts read as datetimes, NaT where a text does not follow the format.

	.. versionadded:: 0.1.0

	Parameters
	----------
	texts
		A text column, without spaces around the texts.
	target_type
		``DATE`` or ``DATETIME``, which sets how texts are read without a format.
	date_format
		How the texts are written, the default of the type when omitted.

	Returns
	-------
	Column
		The datetimes, NaT for a missing text or a text that does not follow the format.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.date_reading import read_moments
	>>> texts = pandas.Series(["2026-12-31 14:30"], dtype="string")
	>>> read_moments(texts, ndp.Type.DATE, None).tolist()
	[NaT]
	>>> read_moments(texts, ndp.Type.DATETIME, None).tolist()
	[Timestamp('2026-12-31 14:30:00')]
	"""
	if isinstance(date_format, CustomDateFormat):
		custom_moments = pandas.to_datetime(texts, format=date_format.pattern, errors="coerce")
		return custom_moments

	if date_format is None:
		default_pattern = DEFAULT_READ_PATTERNS[target_type]
		default_moments = read_date_pattern(texts, default_pattern)
		return default_moments

	common_moments = read_common_format(texts, date_format)

	return common_moments


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
	>>> from numdaplot.conversions.date_reading import read_common_format
	>>> texts = pandas.Series(["2026-12-31T14:30", "31/12/2026"], dtype="string")
	>>> read_common_format(texts, ndp.DateFormat.YEAR_MONTH_DAY_TIME).tolist()
	[Timestamp('2026-12-31 14:30:00'), NaT]
	"""
	read_pattern = READ_PATTERNS[date_format]
	moments = read_date_pattern(texts, read_pattern)

	return moments


def read_date_pattern(texts: Column, read_pattern: str) -> Column:
	"""
	Return texts read with a regular expression naming the parts of a date, NaT where a text does not follow it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	texts
		A text column, without spaces around the texts.
	read_pattern
		The regular expression, whose groups are named after ``DATE_PARTS``. A part it leaves out counts as 0.

	Returns
	-------
	Column
		The datetimes, NaT for a missing text, a text that does not follow the pattern, or an impossible date
		or time such as ``"31/02/2026"`` or ``"25:00"``.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.conversions.date_formats import YEAR_FIRST
	>>> from numdaplot.conversions.date_reading import read_date_pattern
	>>> texts = pandas.Series(["2026-12-31", "31/12/2026"], dtype="string")
	>>> read_date_pattern(texts, YEAR_FIRST).tolist()
	[Timestamp('2026-12-31 00:00:00'), NaT]
	"""
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

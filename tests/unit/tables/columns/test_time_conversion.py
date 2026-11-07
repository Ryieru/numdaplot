"""
Unit tests of the conversion of Table columns to and from times of day.

.. versionadded:: 0.1.0
"""

from datetime import time

import numpy
import pandas
import pytest

from numdaplot.data_types.time_of_day import read_times as read_times_of_day
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.columns.time_conversion import (
	find_time_format_name,
	keep_time_of_day,
	parse_times,
	read_clock_texts,
	read_fraction_microseconds,
	read_times,
	write_times,
)

TIME_DTYPE_NAME = "timedelta64[us]"
CLOCK_TEXTS = pandas.Series([" 15:35 ", "8:05:30", "23:59:59.999999", None], dtype="string")
EXPECTED_CLOCK_TIMES = [time(15, 35), time(8, 5, 30), time(23, 59, 59, 999999), None]
IMPOSSIBLE_TEXTS = pandas.Series(["24:00", "12:60", "12:00:60", "noon", "123:00"], dtype="string")
COMPACT_TEXTS = pandas.Series(["1535", "0805"], dtype="string")
COMPACT_FORMAT = CustomDateFormat("%H%M")
EXPECTED_COMPACT_TIMES = [time(15, 35), time(8, 5)]
REJECTED_TEXTS = pandas.Series(["15:35", "25:00"], dtype="string")
REJECTED_TEXT = "25:00"
FRACTIONS = pandas.Series(["5", "000250", None], dtype=object)
EXPECTED_FRACTIONS = [500000.0, 250.0, 0.0]
MOMENT_INDEX = pandas.DatetimeIndex(["2026-03-14 15:35", "NaT"])
ZONED_MOMENT_INDEX = MOMENT_INDEX.tz_localize("Europe/Paris")
MOMENTS = pandas.Series(MOMENT_INDEX)
ZONED_MOMENTS = pandas.Series(ZONED_MOMENT_INDEX)
EXPECTED_DAY_TIMES = [time(15, 35), None]
STORED_TIMES = pandas.Series(numpy.array([56100250000, "NaT"], dtype="timedelta64[us]"))
EXPECTED_DEFAULT_TEXTS = ["15:35:00.250000", None]
EXPECTED_CUSTOM_TEXTS = ["15h35", None]
WRITTEN_FORMAT = CustomDateFormat("%Hh%M")
DEFAULT_FORMAT_NAME = "HH:MM:SS"


def read_python_times(column: pandas.Series) -> list[time | None]:
	"""
	Return a column of times of day as Python times, None where missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column in ``timedelta64[us]``.

	Returns
	-------
	list[time | None]
		The times of day.
	"""
	stored_values = column.to_numpy(dtype=TIME_DTYPE_NAME)
	python_times = read_times_of_day(stored_values)

	return python_times


def read_present_texts(column: pandas.Series) -> list[str | None]:
	"""
	Return a column of texts, None where missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A text column.

	Returns
	-------
	list[str or None]
		The texts.
	"""
	raw_texts = column.tolist()
	texts = [text if isinstance(text, str) else None for text in raw_texts]

	return texts


def test_parse_times_reads_the_default_clock_texts() -> None:
	"""
	Check HH:MM, H:MM:SS, microseconds, spaces and a missing value.

	.. versionadded:: 0.1.0
	"""
	time_column = parse_times(CLOCK_TEXTS, None)

	times = read_python_times(time_column)
	assert str(time_column.dtype) == TIME_DTYPE_NAME
	assert times == EXPECTED_CLOCK_TIMES


def test_parse_times_reads_a_custom_format() -> None:
	"""
	Check the compact texts of a time without separator.

	.. versionadded:: 0.1.0
	"""
	time_column = parse_times(COMPACT_TEXTS, COMPACT_FORMAT)

	times = read_python_times(time_column)
	assert times == EXPECTED_COMPACT_TIMES


def test_parse_times_names_the_first_rejected_text() -> None:
	"""
	Check that 25:00 raises ValueConversionError with the text.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError) as error_info:
		parse_times(REJECTED_TEXTS, None)

	assert error_info.value.rejected_value == REJECTED_TEXT


def test_read_clock_texts_rejects_impossible_times() -> None:
	"""
	Check hour 24, minute 60, second 60, words and three-digit hours.

	.. versionadded:: 0.1.0
	"""
	times = read_clock_texts(IMPOSSIBLE_TEXTS)

	missing = times.isna()
	assert bool(missing.all())


def test_read_times_uses_the_custom_format_when_given() -> None:
	"""
	Check that the custom pattern replaces the default reading.

	.. versionadded:: 0.1.0
	"""
	default_times = read_times(COMPACT_TEXTS, None)
	custom_times = read_times(COMPACT_TEXTS, COMPACT_FORMAT)

	default_missing = default_times.isna()
	custom_missing = custom_times.isna()
	assert bool(default_missing.all())
	assert not bool(custom_missing.any())


def test_read_fraction_microseconds_pads_the_digits() -> None:
	"""
	Check one digit, six digits and no digit.

	.. versionadded:: 0.1.0
	"""
	microseconds = read_fraction_microseconds(FRACTIONS)

	microsecond_list = microseconds.tolist()
	assert microsecond_list == EXPECTED_FRACTIONS


@pytest.mark.parametrize("moments", [MOMENTS, ZONED_MOMENTS])
def test_keep_time_of_day_gives_the_local_time(moments: pandas.Series) -> None:
	"""
	Check datetimes without and with a time zone.

	.. versionadded:: 0.1.0

	Parameters
	----------
	moments
		A column of datetimes.
	"""
	time_column = keep_time_of_day(moments)

	times = read_python_times(time_column)
	assert times == EXPECTED_DAY_TIMES


def test_write_times_writes_microseconds_only_when_present() -> None:
	"""
	Check the default texts.

	.. versionadded:: 0.1.0
	"""
	text_column = write_times(STORED_TIMES, None)

	texts = read_present_texts(text_column)
	assert texts == EXPECTED_DEFAULT_TEXTS


def test_write_times_follows_a_custom_format() -> None:
	"""
	Check a pattern writing 15h35.

	.. versionadded:: 0.1.0
	"""
	text_column = write_times(STORED_TIMES, WRITTEN_FORMAT)

	texts = read_present_texts(text_column)
	assert texts == EXPECTED_CUSTOM_TEXTS


def test_find_time_format_name_names_the_default_and_custom_formats() -> None:
	"""
	Check both names.

	.. versionadded:: 0.1.0
	"""
	default_name = find_time_format_name(None)
	custom_name = find_time_format_name(COMPACT_FORMAT)

	assert default_name == DEFAULT_FORMAT_NAME
	assert custom_name == COMPACT_FORMAT.pattern

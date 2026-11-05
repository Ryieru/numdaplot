"""
Unit tests of the conversion of Table columns between texts, dates, datetimes and durations.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

import numpy
import pandas
import pytest

from numdaplot.data_types.type import Type
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_format import DateFormat
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.columns.date_conversion import (
	YEAR_FIRST,
	convert_moments,
	find_format_name,
	has_time,
	parse_dates,
	read_common_format,
	read_date_pattern,
	read_moments,
	write_dates,
	write_durations,
)
from numdaplot.tables.frames.column_values import find_column_type

TEXT_DTYPE = "string"
DECEMBER_LAST = pandas.Timestamp("2026-12-31")
DECEMBER_LAST_AFTERNOON = pandas.Timestamp("2026-12-31 14:30")
DECEMBER_LAST_SECONDS = pandas.Timestamp("2026-12-31 14:30:15")
FEBRUARY_FIRST = pandas.Timestamp("2026-02-01")
DAY_MONTH_PATTERN = CustomDateFormat("%d %b %Y")
DAY_TIME_PATTERN = CustomDateFormat("%d/%m/%Y %H:%M")
DAYS = pandas.Series(numpy.array(["2026-12-31", "NaT"], dtype="datetime64[s]"))
TIMES = pandas.Series(pandas.to_datetime(["2026-12-31 14:30:15"])).astype("datetime64[ns]")
PARIS_TIMES = TIMES.dt.tz_localize("Europe/Paris")
DURATIONS = pandas.Series(numpy.array([36, "NaT", -12], dtype="timedelta64[h]").astype("timedelta64[ns]"))
EXPECTED_DAY_TEXTS = ["31/12/2026", None]
EXPECTED_DEFAULT_DAY_TEXTS = ["2026-12-31", None]
EXPECTED_DEFAULT_TIME_TEXTS = ["2026-12-31 14:30:15"]
EXPECTED_PARIS_TEXTS = ["31/12/2026 14:30:15+01:00"]
EXPECTED_CUSTOM_TEXTS = ["31 Dec 2026"]
EXPECTED_DURATION_TEXTS = ["1 days 12:00:00", None, "-1 days +12:00:00"]
EXPECTED_MIDNIGHT = [pandas.Timestamp("2026-12-31")]
REJECTED_TEXT = "31/02/2026"
DAY_TEXT = "2026-12-31"
DAY_TIME_TEXT = "2026-12-31 14:30"
DAY_T_TIME_TEXT = "2026-12-31T14:30"
DAY_SECONDS_TEXT = "2026-12-31 14:30:15"
FIRST_DAY_NAME = "YEAR_MONTH_DAY"
FIRST_TIME_NAME = "YEAR_MONTH_DAY_TIME"
CUSTOM_PATTERN_TEXT = "%d %b %Y"
EXPECTED_DEFAULT_DATE_MESSAGE = (
	"Cannot read the TEXT value '2026-12-31 14:30' as DATE with the format YEAR_MONTH_DAY. "
	"Give the format of the column with format=, using DateFormat or CustomDateFormat."
)
EXPECTED_DEFAULT_TIME_MESSAGE = (
	"Cannot read the TEXT value '31/02/2026' as DATETIME with the format YEAR_MONTH_DAY_TIME. "
	"Give the format of the column with format=, using DateFormat or CustomDateFormat."
)
EXPECTED_CUSTOM_MESSAGE = (
	"Cannot read the TEXT value '31/02/2026' as DATE with the format %d %b %Y. "
	"Give the format of the column with format=, using DateFormat or CustomDateFormat."
)


@dataclass(frozen=True)
class ReadCase:
	"""
	A text read with a format, and the expected datetime.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text
		The text.
	date_format
		The format.
	expected_moment
		The datetime read.
	"""

	text: str
	date_format: DateFormat
	expected_moment: pandas.Timestamp


READ_CASES = [
	ReadCase("31/12/2026", DateFormat.DAY_MONTH_YEAR, DECEMBER_LAST),
	ReadCase("1.2.2026", DateFormat.DAY_MONTH_YEAR, FEBRUARY_FIRST),
	ReadCase("12-31-2026", DateFormat.MONTH_DAY_YEAR, DECEMBER_LAST),
	ReadCase("2026/12/31", DateFormat.YEAR_MONTH_DAY, DECEMBER_LAST),
	ReadCase("31/12/2026 14:30", DateFormat.DAY_MONTH_YEAR_TIME, DECEMBER_LAST_AFTERNOON),
	ReadCase("12/31/2026 14:30:15", DateFormat.MONTH_DAY_YEAR_TIME, DECEMBER_LAST_SECONDS),
	ReadCase("2026-12-31T14:30", DateFormat.YEAR_MONTH_DAY_TIME, DECEMBER_LAST_AFTERNOON),
	ReadCase("2026-12-31 14:30:15", DateFormat.YEAR_MONTH_DAY_TIME, DECEMBER_LAST_SECONDS),
]
UNREADABLE_CASES = [
	("31/12-2026", DateFormat.DAY_MONTH_YEAR),
	("31/02/2026", DateFormat.DAY_MONTH_YEAR),
	("31/12/26", DateFormat.DAY_MONTH_YEAR),
	("31/12/2026 14:30", DateFormat.DAY_MONTH_YEAR),
	("31/12/2026", DateFormat.DAY_MONTH_YEAR_TIME),
	("31/12/2026T14:30", DateFormat.DAY_MONTH_YEAR_TIME),
	("2026-12-31 25:00", DateFormat.YEAR_MONTH_DAY_TIME),
	("2026-12-31 10:60", DateFormat.YEAR_MONTH_DAY_TIME),
]


def read_texts(texts: pandas.Series) -> list[str | None]:
	"""
	Return the texts of a column, None for a missing text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	texts
		A text column.

	Returns
	-------
	list[str | None]
		The texts.
	"""
	text_list = [None if pandas.isna(text) else str(text) for text in texts]

	return text_list


@pytest.mark.parametrize("case", READ_CASES)
def test_read_common_format_reads_each_format(case: ReadCase) -> None:
	"""
	Check each common format with its separators and optional seconds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	case
		The text, the format and the expected datetime.
	"""
	texts = pandas.Series([case.text], dtype=TEXT_DTYPE)

	moments = read_common_format(texts, case.date_format)

	assert moments.iloc[0] == case.expected_moment


@pytest.mark.parametrize(("text", "date_format"), UNREADABLE_CASES)
def test_read_common_format_gives_nat_for_a_text_that_does_not_fit(text: str, date_format: DateFormat) -> None:
	"""
	Check mixed separators, impossible dates and times, short years and a missing or extra time.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text
		A text that the format cannot read.
	date_format
		The format.
	"""
	texts = pandas.Series([text], dtype=TEXT_DTYPE)

	moments = read_common_format(texts, date_format)

	missing_moments = moments.isna()
	is_missing = bool(missing_moments.iloc[0])
	assert is_missing


def test_parse_dates_reads_dates_and_keeps_missing_texts() -> None:
	"""
	Check the type and the values of dates read from texts.

	.. versionadded:: 0.1.0
	"""
	texts = pandas.Series(["31/12/2026", None], dtype=TEXT_DTYPE)

	dates = parse_dates(texts, Type.DATE, DateFormat.DAY_MONTH_YEAR)

	date_type = find_column_type(dates)
	missing = dates.isna()
	is_second_missing = bool(missing.iloc[1])
	assert date_type == Type.DATE
	assert dates.iloc[0] == DECEMBER_LAST
	assert is_second_missing


def test_parse_dates_reads_a_custom_pattern_with_english_months() -> None:
	"""
	Check a custom pattern.

	.. versionadded:: 0.1.0
	"""
	texts = pandas.Series(["31 Dec 2026"], dtype=TEXT_DTYPE)

	dates = parse_dates(texts, Type.DATE, DAY_MONTH_PATTERN)

	assert dates.iloc[0] == DECEMBER_LAST


def test_parse_dates_cites_the_first_unreadable_text() -> None:
	"""
	Check that an impossible date raises ValueConversionError citing it.

	.. versionadded:: 0.1.0
	"""
	texts = pandas.Series(["31/12/2026", REJECTED_TEXT], dtype=TEXT_DTYPE)

	with pytest.raises(ValueConversionError) as caught:
		parse_dates(texts, Type.DATE, DateFormat.DAY_MONTH_YEAR)

	assert caught.value.rejected_value == REJECTED_TEXT


def test_write_dates_writes_dates_in_a_format() -> None:
	"""
	Check dates written day first, a missing date staying missing.

	.. versionadded:: 0.1.0
	"""
	texts = write_dates(DAYS, DateFormat.DAY_MONTH_YEAR)

	text_list = read_texts(texts)
	assert text_list == EXPECTED_DAY_TEXTS


def test_write_dates_uses_year_month_day_by_default() -> None:
	"""
	Check the default texts of dates and of datetimes.

	.. versionadded:: 0.1.0
	"""
	day_texts = write_dates(DAYS, None)
	time_texts = write_dates(TIMES, None)

	day_list = read_texts(day_texts)
	time_list = time_texts.tolist()
	assert day_list == EXPECTED_DEFAULT_DAY_TEXTS
	assert time_list == EXPECTED_DEFAULT_TIME_TEXTS


def test_write_dates_adds_the_offset_of_a_zone() -> None:
	"""
	Check that a datetime with a zone is written with its offset.

	.. versionadded:: 0.1.0
	"""
	texts = write_dates(PARIS_TIMES, DateFormat.DAY_MONTH_YEAR_TIME)

	text_list = texts.tolist()
	assert text_list == EXPECTED_PARIS_TEXTS


def test_write_dates_follows_a_custom_pattern() -> None:
	"""
	Check a custom pattern, without offset.

	.. versionadded:: 0.1.0
	"""
	texts = write_dates(PARIS_TIMES, DAY_MONTH_PATTERN)

	text_list = texts.tolist()
	assert text_list == EXPECTED_CUSTOM_TEXTS


def test_write_durations_writes_durations_as_pandas() -> None:
	"""
	Check durations, a missing one staying missing.

	.. versionadded:: 0.1.0
	"""
	texts = write_durations(DURATIONS)

	text_list = read_texts(texts)
	assert text_list == EXPECTED_DURATION_TEXTS


def test_convert_moments_gives_the_date_of_datetimes() -> None:
	"""
	Check that a datetime gives its date, in its zone, as a DATE column.

	.. versionadded:: 0.1.0
	"""
	dates = convert_moments(PARIS_TIMES, Type.DATE)

	date_type = find_column_type(dates)
	date_list = dates.tolist()
	assert date_type == Type.DATE
	assert date_list == EXPECTED_MIDNIGHT


def test_convert_moments_gives_dates_at_midnight() -> None:
	"""
	Check that a date becomes a DATETIME column.

	.. versionadded:: 0.1.0
	"""
	datetimes = convert_moments(DAYS, Type.DATETIME)

	datetime_type = find_column_type(datetimes)
	assert datetime_type == Type.DATETIME


@pytest.mark.parametrize(
	("date_format", "expected"),
	[
		(DateFormat.DAY_MONTH_YEAR, False),
		(DateFormat.YEAR_MONTH_DAY_TIME, True),
		(DAY_TIME_PATTERN, True),
		(DAY_MONTH_PATTERN, False),
	],
)
def test_has_time_tells_the_formats_with_a_time(date_format: DateFormat | CustomDateFormat, expected: bool) -> None:
	"""
	Check common formats and a custom pattern.

	.. versionadded:: 0.1.0

	Parameters
	----------
	date_format
		A format.
	expected
		Whether it has a time.
	"""
	format_has_time = has_time(date_format)

	assert format_has_time == expected


def test_read_moments_without_format_reads_datetimes_with_or_without_time() -> None:
	"""
	Check that a datetime column without format reads each text with its own time, midnight without one.

	.. versionadded:: 0.1.0
	"""
	texts = pandas.Series([DAY_SECONDS_TEXT, DAY_T_TIME_TEXT, DAY_TEXT], dtype=TEXT_DTYPE)

	moments = read_moments(texts, Type.DATETIME, None)

	moment_list = moments.tolist()
	assert moment_list == [DECEMBER_LAST_SECONDS, DECEMBER_LAST_AFTERNOON, DECEMBER_LAST]


def test_read_moments_without_format_leaves_the_time_out_of_dates() -> None:
	"""
	Check that a date column without format gives NaT for a text with a time.

	.. versionadded:: 0.1.0
	"""
	texts = pandas.Series([DAY_TIME_TEXT], dtype=TEXT_DTYPE)

	moments = read_moments(texts, Type.DATE, None)

	assert moments.isna().all()


def test_read_moments_with_a_time_format_needs_the_time() -> None:
	"""
	Check that a given format with time gives NaT for a text without time.

	.. versionadded:: 0.1.0
	"""
	texts = pandas.Series([DAY_TEXT], dtype=TEXT_DTYPE)

	moments = read_moments(texts, Type.DATETIME, DateFormat.YEAR_MONTH_DAY_TIME)

	assert moments.isna().all()


def test_read_moments_reads_a_custom_pattern() -> None:
	"""
	Check that a custom format is read with its pattern.

	.. versionadded:: 0.1.0
	"""
	texts = pandas.Series(["31 Dec 2026"], dtype=TEXT_DTYPE)

	moments = read_moments(texts, Type.DATE, DAY_MONTH_PATTERN)

	moment_list = moments.tolist()
	assert moment_list == EXPECTED_MIDNIGHT


def test_read_date_pattern_counts_the_missing_clock_parts_as_zero() -> None:
	"""
	Check that a pattern without clock gives midnight, and NaT for a text it does not follow.

	.. versionadded:: 0.1.0
	"""
	texts = pandas.Series([DAY_TEXT, REJECTED_TEXT], dtype=TEXT_DTYPE)

	moments = read_date_pattern(texts, YEAR_FIRST)

	first_moment = moments.iloc[0]
	assert first_moment == DECEMBER_LAST
	assert moments.isna().iloc[1]


def test_find_format_name_gives_the_default_of_each_type() -> None:
	"""
	Check the name of the default format of dates and datetimes.

	.. versionadded:: 0.1.0
	"""
	date_name = find_format_name(Type.DATE, None)
	time_name = find_format_name(Type.DATETIME, None)

	assert date_name == FIRST_DAY_NAME
	assert time_name == FIRST_TIME_NAME


def test_find_format_name_gives_the_given_format() -> None:
	"""
	Check that a common format gives its name and a custom format gives its pattern.

	.. versionadded:: 0.1.0
	"""
	common_name = find_format_name(Type.DATETIME, DateFormat.DAY_MONTH_YEAR)
	custom_name = find_format_name(Type.DATE, DAY_MONTH_PATTERN)

	assert common_name == DateFormat.DAY_MONTH_YEAR.name
	assert custom_name == CUSTOM_PATTERN_TEXT


def test_parse_dates_keeps_a_missing_text_missing_without_format() -> None:
	"""
	Check that a missing text stays missing in a datetime column read without format.

	.. versionadded:: 0.1.0
	"""
	texts = pandas.Series([DAY_TIME_TEXT, None], dtype=TEXT_DTYPE)

	dates = parse_dates(texts, Type.DATETIME, None)

	assert find_column_type(dates) == Type.DATETIME
	assert dates.iloc[0] == DECEMBER_LAST_AFTERNOON
	assert dates.isna().iloc[1]


def test_parse_dates_refusal_of_a_time_as_date_names_the_default_format() -> None:
	"""
	Check the message when a date column read without format holds a time.

	.. versionadded:: 0.1.0
	"""
	texts = pandas.Series([DAY_TIME_TEXT], dtype=TEXT_DTYPE)

	with pytest.raises(ValueConversionError) as caught_error:
		parse_dates(texts, Type.DATE, None)

	error_text = str(caught_error.value)
	assert error_text == EXPECTED_DEFAULT_DATE_MESSAGE


def test_parse_dates_refusal_without_format_names_the_default_of_datetimes() -> None:
	"""
	Check the message when a datetime column read without format holds another way of writing dates.

	.. versionadded:: 0.1.0
	"""
	texts = pandas.Series([REJECTED_TEXT], dtype=TEXT_DTYPE)

	with pytest.raises(ValueConversionError) as caught_error:
		parse_dates(texts, Type.DATETIME, None)

	error_text = str(caught_error.value)
	assert error_text == EXPECTED_DEFAULT_TIME_MESSAGE


def test_parse_dates_refusal_with_a_custom_format_shows_its_pattern() -> None:
	"""
	Check that the message names the pattern of a custom format.

	.. versionadded:: 0.1.0
	"""
	texts = pandas.Series([REJECTED_TEXT], dtype=TEXT_DTYPE)

	with pytest.raises(ValueConversionError) as caught_error:
		parse_dates(texts, Type.DATE, DAY_MONTH_PATTERN)

	error_text = str(caught_error.value)
	assert error_text == EXPECTED_CUSTOM_MESSAGE

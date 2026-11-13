"""
Unit tests of the reading of texts as dates and datetimes.

.. versionadded:: 0.2.0
"""

from dataclasses import dataclass

import pandas
import pytest

from numdaplot.conversions import date_reading
from numdaplot.conversions.date_formats import YEAR_FIRST
from numdaplot.conversions.date_reading import parse_dates, read_common_format, read_date_pattern, read_moments
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_format import DateFormat
from numdaplot.errors.time_overflow_error import TimeOverflowError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.frames.column_values import find_column_type
from numdaplot.types.type import Type

FEBRUARY_FIRST = pandas.Timestamp("2026-02-01")
DECEMBER_LAST = pandas.Timestamp("2026-12-31")
DECEMBER_LAST_AFTERNOON = pandas.Timestamp("2026-12-31 14:30")
DECEMBER_LAST_SECONDS = pandas.Timestamp("2026-12-31 14:30:15")
DAY_MONTH_PATTERN = CustomDateFormat("%d %b %Y")
EXPECTED_MIDNIGHT = [pandas.Timestamp("2026-12-31")]
TEXT_DTYPE = "string"
REJECTED_TEXT = "31/02/2026"
FAR_DAY_TEXT = "3000-01-01"
READ_MOMENTS_NAME = "read_moments"
DAY_TEXT = "2026-12-31"
DAY_TIME_TEXT = "2026-12-31 14:30"
DAY_T_TIME_TEXT = "2026-12-31T14:30"
DAY_SECONDS_TEXT = "2026-12-31 14:30:15"
EXPECTED_DEFAULT_DATE_MESSAGE = (
	"Cannot read the TEXT value '2026-12-31 14:30' as DATE with the format YEAR_MONTH_DAY. "
	"Give the format of the values with format=, using DateFormat or CustomDateFormat."
)
EXPECTED_DEFAULT_TIME_MESSAGE = (
	"Cannot read the TEXT value '31/02/2026' as DATETIME with the format YEAR_MONTH_DAY_TIME. "
	"Give the format of the values with format=, using DateFormat or CustomDateFormat."
)
EXPECTED_CUSTOM_MESSAGE = (
	"Cannot read the TEXT value '31/02/2026' as DATE with the format %d %b %Y. "
	"Give the format of the values with format=, using DateFormat or CustomDateFormat."
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


def read_no_moment(texts: pandas.Series, target_type: Type, date_format: DateFormat | None) -> pandas.Series:
	"""
	Fake reading giving a missing moment for every text, as pandas does for a date beyond its range.

	.. versionadded:: 0.1.0

	Parameters
	----------
	texts
		The texts read.
	target_type
		Ignored.
	date_format
		Ignored.

	Returns
	-------
	pandas.Series
		NaT for each text.
	"""
	text_count = len(texts)
	missing_moments = [pandas.NaT] * text_count
	moments = pandas.Series(missing_moments, dtype="datetime64[ns]")

	return moments


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


def test_parse_dates_refuses_a_date_beyond_the_range_pandas_reads_as_missing(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that a date beyond about 2262 that pandas leaves missing raises TimeOverflowError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the reading of the moments with a fake.
	"""
	monkeypatch.setattr(date_reading, READ_MOMENTS_NAME, read_no_moment)
	texts = pandas.Series([FAR_DAY_TEXT], dtype=TEXT_DTYPE)

	with pytest.raises(TimeOverflowError):
		parse_dates(texts, Type.DATE, None)

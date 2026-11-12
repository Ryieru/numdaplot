"""
Unit tests of the conversion of Table columns between texts, dates, datetimes and durations.

.. versionadded:: 0.1.0
"""

import numpy
import pandas

from numdaplot.conversions.date_conversion import convert_moments, write_dates, write_durations
from numdaplot.data_types.type import Type
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_format import DateFormat
from numdaplot.tables.frames.column_values import find_column_type

DAY_MONTH_PATTERN = CustomDateFormat("%d %b %Y")
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

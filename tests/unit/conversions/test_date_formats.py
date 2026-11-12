"""
Unit tests of what a date format holds, and how it is read and named.

.. versionadded:: 0.2.0
"""

import pytest

from numdaplot.conversions.date_formats import find_format_name, has_date, has_time
from numdaplot.data_types.type import Type
from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_format import DateFormat

DAY_MONTH_PATTERN = CustomDateFormat("%d %b %Y")
DAY_TIME_PATTERN = CustomDateFormat("%d/%m/%Y %H:%M")
FIRST_DAY_NAME = "YEAR_MONTH_DAY"
FIRST_TIME_NAME = "YEAR_MONTH_DAY_TIME"
CUSTOM_PATTERN_TEXT = "%d %b %Y"


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


def test_has_date_is_false_only_for_a_time_pattern() -> None:
	"""
	Check a common format, a pattern with a date and a pattern of a time.

	.. versionadded:: 0.1.0
	"""
	common_has_date = has_date(DateFormat.DAY_MONTH_YEAR)
	date_pattern_has_date = has_date(CustomDateFormat("%d/%m/%Y"))
	time_pattern_has_date = has_date(CustomDateFormat("%H:%M"))

	assert common_has_date
	assert date_pattern_has_date
	assert not time_pattern_has_date

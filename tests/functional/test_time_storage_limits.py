"""
Functional tests of dates, datetimes and durations stored out of their range.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime, timedelta

import numpy
import pytest

import numdaplot as ndp

ONE_DAY = timedelta(days=1)
DAYS_BEYOND_RANGE = 200000
FACTOR_ABOVE_SIGNED_INTEGERS = 2**63
START_DATETIME = datetime(2020, 1, 1)
FAR_DATETIME = datetime(3000, 1, 1)
FAR_DATE = date(3000, 1, 1)
OLD_DATETIME = datetime(1600, 1, 1)
LAST_DATETIME = datetime(2262, 4, 11, 23, 47, 16)
FIRST_DATETIME = datetime(1677, 9, 21, 0, 12, 44)
LONGEST_DURATION = timedelta(days=106751)
DAYS_OF_THREE_HUNDRED_YEARS = 110000
ONE_DAY_UNIT = ndp.DurationUnit.DAY
FAR_TEXT = "3000-01-01 10:00:00"
IMPOSSIBLE_FAR_TEXT = "3000-02-31"
COLUMN_NAME = "when"
DATETIME_MESSAGE = "The operation from_list gives values outside the range of DATETIME, from 1677 to 2262."
CONVERT_MESSAGE = (
	"The operation convert gives values of the column 'when' outside the range of DATETIME, from 1677 to 2262."
)


@pytest.mark.parametrize("far_value", [FAR_DATETIME, OLD_DATETIME, timedelta(days=DAYS_BEYOND_RANGE)])
def test_from_list_refuses_a_value_out_of_range(far_value: datetime | timedelta) -> None:
	"""
	Check that a value is not stored as a wrong datetime or duration.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.TimeOverflowError):
		ndp.Array.from_list([far_value])


def test_from_list_names_the_range_of_datetimes() -> None:
	"""
	Check the message of a datetime out of range.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.TimeOverflowError) as error_info:
		ndp.Array.from_list([FAR_DATETIME])

	error_text = str(error_info.value)
	assert error_text == DATETIME_MESSAGE


def test_from_list_refuses_a_date_stored_as_datetime_out_of_range() -> None:
	"""
	Check a date that fits ``DATE`` but not the requested ``DATETIME``.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.TimeOverflowError):
		ndp.Array.from_list([FAR_DATE], dtype=ndp.Type.DATETIME)


@pytest.mark.parametrize("edge_value", [LAST_DATETIME, FIRST_DATETIME, LONGEST_DURATION, -LONGEST_DURATION])
def test_from_list_keeps_the_last_values_of_the_range(edge_value: datetime | timedelta) -> None:
	"""
	Check that the limits themselves stay accepted.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([edge_value])

	value_list = values.to_list()
	assert value_list == [edge_value]


def test_filled_refuses_a_value_out_of_range() -> None:
	"""
	Check that ``Array.filled`` follows ``Array.from_list``.

	.. versionadded:: 0.1.0
	"""
	shape = ndp.Shape([2])

	with pytest.raises(ndp.TimeOverflowError):
		ndp.Array.filled(shape, FAR_DATETIME)


def test_replace_refuses_a_value_out_of_range() -> None:
	"""
	Check that ``Array.replace`` does not store a wrong datetime.

	.. versionadded:: 0.1.0
	"""
	moments = ndp.Array.from_list([START_DATETIME])
	first_moment = ndp.Region(rows=ndp.Index(0))
	replacement = ndp.Replacement(region=first_moment, value=FAR_DATETIME)

	with pytest.raises(ndp.TimeOverflowError):
		moments.replace(replacement)


@pytest.mark.parametrize(
	"numbers",
	[
		[DAYS_OF_THREE_HUNDRED_YEARS],
		[-DAYS_OF_THREE_HUNDRED_YEARS],
		[2**62],
		[float(DAYS_OF_THREE_HUNDRED_YEARS)],
		[numpy.inf],
	],
)
def test_to_duration_refuses_a_number_out_of_range(numbers: list[int] | list[float]) -> None:
	"""
	Check integers and decimals read as durations too large.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list(numbers)
	function = ndp.ToDuration(unit=ONE_DAY_UNIT)

	with pytest.raises(ndp.TimeOverflowError):
		values.apply(function)


def test_to_duration_refuses_unsigned_integers_above_signed_integers() -> None:
	"""
	Check that a ``UINT64`` number does not wrap around before being read as a duration.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([FACTOR_ABOVE_SIGNED_INTEGERS], dtype=ndp.Type.UINT64)
	function = ndp.ToDuration(unit=ndp.DurationUnit.SECOND)

	with pytest.raises(ndp.TimeOverflowError):
		values.apply(function)


def test_to_duration_keeps_missing_numbers_missing() -> None:
	"""
	Check that a missing number is never out of range.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([None, 1.0])
	function = ndp.ToDuration(unit=ONE_DAY_UNIT)

	durations = values.apply(function)

	duration_list = durations.to_list()
	assert duration_list == [None, ONE_DAY]


def build_text_table(text: str) -> ndp.Table:
	"""
	Return a Table with one text column holding one text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	text
		The text of the column.

	Returns
	-------
	ndp.Table
		The Table.
	"""
	texts = ndp.Array.from_list([text])
	table = ndp.Table.from_arrays({COLUMN_NAME: texts})

	return table


@pytest.mark.parametrize(
	"date_format",
	[None, ndp.DateFormat.YEAR_MONTH_DAY_TIME, ndp.CustomDateFormat("%Y-%m-%d %H:%M:%S")],
)
def test_convert_refuses_a_text_read_as_a_datetime_out_of_range(
	date_format: ndp.DateFormat | ndp.CustomDateFormat | None,
) -> None:
	"""
	Check every way to read a text with the same error on every version of pandas.

	.. versionadded:: 0.1.0
	"""
	table = build_text_table(FAR_TEXT)
	conversion = ndp.Conversion(column=COLUMN_NAME, dtype=ndp.Type.DATETIME, format=date_format)

	with pytest.raises(ndp.TimeOverflowError):
		table.convert(conversion)


def test_convert_names_the_column_out_of_range() -> None:
	"""
	Check the message of a column out of range.

	.. versionadded:: 0.1.0
	"""
	table = build_text_table(FAR_TEXT)
	conversion = ndp.Conversion(column=COLUMN_NAME, dtype=ndp.Type.DATETIME)

	with pytest.raises(ndp.TimeOverflowError) as error_info:
		table.convert(conversion)

	error_text = str(error_info.value)
	assert error_text == CONVERT_MESSAGE


def test_convert_refuses_dates_out_of_range_as_datetimes() -> None:
	"""
	Check dates that ``DATE`` holds but ``DATETIME`` cannot.

	.. versionadded:: 0.1.0
	"""
	dates = ndp.Array.from_list([FAR_DATE])
	table = ndp.Table.from_arrays({COLUMN_NAME: dates})
	conversion = ndp.Conversion(column=COLUMN_NAME, dtype=ndp.Type.DATETIME)

	with pytest.raises(ndp.TimeOverflowError):
		table.convert(conversion)


def test_convert_still_refuses_an_impossible_date_as_unreadable() -> None:
	"""
	Check that a text that is not a real date keeps its error, whatever its year.

	.. versionadded:: 0.1.0
	"""
	table = build_text_table(IMPOSSIBLE_FAR_TEXT)
	conversion = ndp.Conversion(column=COLUMN_NAME, dtype=ndp.Type.DATETIME)

	with pytest.raises(ndp.ValueConversionError):
		table.convert(conversion)

"""
Functional tests of dates built from their day, their month and their year.

.. versionadded:: 0.1.0
"""

from datetime import date
from typing import Any

import pytest

import numdaplot as ndp

DAYS = [14, 29, 1]
MONTHS = [7, 2, 1]
YEARS = [2025, 2024, 25]
EXPECTED_DATES = [date(2025, 7, 14), date(2024, 2, 29), date(25, 1, 1)]
DECIMAL_DAYS = [14.0, None]
DECIMAL_MONTHS = [7.0, 8.0]
DECIMAL_YEARS = [2025.0, 2025.0]
EXPECTED_MISSING_DATES = [date(2025, 7, 14), None]
FEBRUARY_DAYS = [28, 31]
FEBRUARY_MONTHS = [2, 2]
FEBRUARY_YEARS = [2025, 2025]
EXPECTED_FEBRUARY_MESSAGE = "Cannot build a DATE from the year 2025, the month 2 and the day 31."
HALF_DAYS = [3.5]
ONE_MONTH = [3.0]
ONE_YEAR = [2025.0]
EXPECTED_HALF_DAY_MESSAGE = "Cannot use the FLOAT64 value 3.5 as a day: date parts must be whole numbers."


def build_parts(days: list[Any], months: list[Any], years: list[Any]) -> ndp.DateParts:
	"""
	Return the date parts of an accident Table with the columns jour, mois and an.

	.. versionadded:: 0.1.0

	Parameters
	----------
	days
		The jour column.
	months
		The mois column.
	years
		The an column.

	Returns
	-------
	ndp.DateParts
		The parts read from the columns of the Table.
	"""
	day_array = ndp.Array.from_list(days)
	month_array = ndp.Array.from_list(months)
	year_array = ndp.Array.from_list(years)
	accidents = ndp.Table.from_arrays({"jour": day_array, "mois": month_array, "an": year_array})
	day_column = accidents.column("jour")
	month_column = accidents.column("mois")
	year_column = accidents.column("an")
	parts = ndp.DateParts(year=year_column, month=month_column, day=day_column)

	return parts


def test_three_columns_become_a_column_of_dates() -> None:
	"""
	Check the BAAC use: jour, mois and an become one DATE column of the Table, the year 25 kept as written.

	.. versionadded:: 0.1.0
	"""
	parts = build_parts(DAYS, MONTHS, YEARS)

	dates = ndp.Array.from_date_parts(parts)
	accidents = ndp.Table.from_arrays({"date": dates})

	date_column = accidents.column("date")
	date_list = date_column.to_list()
	assert accidents.column_types["date"] == ndp.Type.DATE
	assert date_list == EXPECTED_DATES


def test_a_missing_day_gives_a_missing_date() -> None:
	"""
	Check that a decimal column with a missing day gives a missing date.

	.. versionadded:: 0.1.0
	"""
	parts = build_parts(DECIMAL_DAYS, DECIMAL_MONTHS, DECIMAL_YEARS)

	dates = ndp.Array.from_date_parts(parts)

	date_list = dates.to_list()
	assert date_list == EXPECTED_MISSING_DATES


def test_an_impossible_date_is_named_in_the_error() -> None:
	"""
	Check the message of the 31st of February.

	.. versionadded:: 0.1.0
	"""
	parts = build_parts(FEBRUARY_DAYS, FEBRUARY_MONTHS, FEBRUARY_YEARS)

	with pytest.raises(ndp.ValueConversionError) as error_info:
		ndp.Array.from_date_parts(parts)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_FEBRUARY_MESSAGE


def test_a_day_that_is_not_whole_is_named_in_the_error() -> None:
	"""
	Check the message of the day 3.5.

	.. versionadded:: 0.1.0
	"""
	parts = build_parts(HALF_DAYS, ONE_MONTH, ONE_YEAR)

	with pytest.raises(ndp.ValueConversionError) as error_info:
		ndp.Array.from_date_parts(parts)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_HALF_DAY_MESSAGE

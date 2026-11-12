"""
Functional tests of dates in a Table: conversions, formats, periods and files.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime
from pathlib import Path

import pytest

import numdaplot as ndp

DAY_TEXTS = ["31/12/2026", "1.2.2026"]
ISO_DAY_TEXTS = ["2026-12-31", "2026-02-01"]
EXPECTED_DAYS = [date(2026, 12, 31), date(2026, 2, 1)]
EXPECTED_WRITTEN_DAYS = ["31/12/2026", "01/02/2026"]
IMPOSSIBLE_DAY = "31/02/2026"
PICKUP_TEXTS = ["2019-03-23 20:21:09", "2019-03-24T08:15", "2019-03-25"]
EXPECTED_PICKUPS = [datetime(2019, 3, 23, 20, 21, 9), datetime(2019, 3, 24, 8, 15), datetime(2019, 3, 25)]
PICKUP_DAY = "2019-03-25"
PICKUP_TIME = "2019-03-23 20:21:09"
THROUGH_DATETIME_HINT = "Convert the values to DATETIME first"
TRIPS_CSV_NAME = "trips.csv"
MIDNIGHT_PICKUPS = [datetime(2019, 3, 23), datetime(2019, 3, 24)]
VARIED_PICKUPS = [datetime(2019, 3, 23), datetime(2019, 3, 24, 8, 15)]
SALE_DAYS = [date(2026, 1, 5), date(2026, 1, 28), date(2026, 2, 3)]
SALE_PRICES = [10.0, 20.0, 5.0]
EXPECTED_MONTHS = [date(2026, 1, 1), date(2026, 2, 1)]
EXPECTED_MONTH_TOTALS = [30.0, 5.0]


def build_text_days(texts: list[str]) -> ndp.Table:
	"""
	Return a Table of one text column named day.

	.. versionadded:: 0.1.0

	Parameters
	----------
	texts
		The texts of the column.

	Returns
	-------
	ndp.Table
		The Table.
	"""
	text_array = ndp.Array.from_list(texts)
	text_days = ndp.Table.from_arrays({"day": text_array})

	return text_days


def test_texts_written_day_first_become_dates() -> None:
	"""
	Check dates read day first, with two separators.

	.. versionadded:: 0.1.0
	"""
	text_days = build_text_days(DAY_TEXTS)
	day_first = ndp.TableConversion(column="day", dtype=ndp.Type.DATE, format=ndp.DateFormat.DAY_MONTH_YEAR)

	days = text_days.convert(day_first)

	day_array = days.column("day")
	day_list = day_array.to_list()
	assert day_list == EXPECTED_DAYS


def test_texts_without_format_are_read_year_first() -> None:
	"""
	Check the default format.

	.. versionadded:: 0.1.0
	"""
	text_days = build_text_days(ISO_DAY_TEXTS)

	days = text_days.convert(ndp.TableConversion(column="day", dtype=ndp.Type.DATE))

	day_array = days.column("day")
	day_list = day_array.to_list()
	assert day_list == EXPECTED_DAYS


def test_an_impossible_date_is_cited() -> None:
	"""
	Check that February 31 raises ValueConversionError citing the text.

	.. versionadded:: 0.1.0
	"""
	text_days = build_text_days([IMPOSSIBLE_DAY])
	day_first = ndp.TableConversion(column="day", dtype=ndp.Type.DATE, format=ndp.DateFormat.DAY_MONTH_YEAR)

	with pytest.raises(ndp.ValueConversionError) as caught:
		text_days.convert(day_first)

	assert caught.value.rejected_value == IMPOSSIBLE_DAY


def test_dates_are_written_in_a_format() -> None:
	"""
	Check dates written back day first.

	.. versionadded:: 0.1.0
	"""
	text_days = build_text_days(ISO_DAY_TEXTS)
	days = text_days.convert(ndp.TableConversion(column="day", dtype=ndp.Type.DATE))
	day_first = ndp.TableConversion(column="day", dtype=ndp.Type.TEXT, format=ndp.DateFormat.DAY_MONTH_YEAR)

	written_days = days.convert(day_first)

	written_array = written_days.column("day")
	written_list = written_array.to_list()
	assert written_list == EXPECTED_WRITTEN_DAYS


def test_a_format_on_numbers_is_refused() -> None:
	"""
	Check that a format given to a number conversion raises InvalidConversionError.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Table.from_arrays({"price": ndp.Array.from_list(SALE_PRICES)})
	price_texts = ndp.TableConversion(column="price", dtype=ndp.Type.TEXT, format=ndp.DateFormat.DAY_MONTH_YEAR)

	with pytest.raises(ndp.InvalidConversionError):
		prices.convert(price_texts)


def test_sales_are_grouped_by_month_through_a_period_column() -> None:
	"""
	Check the total of each month, computed from a DatePeriod column added to the Table.

	.. versionadded:: 0.1.0
	"""
	sale_days = ndp.Array.from_list(SALE_DAYS)
	prices = ndp.Array.from_list(SALE_PRICES)
	sales = ndp.Table.from_arrays({"day": sale_days, "price": prices})
	months = sale_days.apply(ndp.DatePeriod(unit=ndp.PeriodUnit.MONTH))
	sales_with_month = sales.add_column(ndp.NewColumn(name="month", values=months))
	total = ndp.Calculation(column="price", function=ndp.Sum())

	monthly_totals = sales_with_month.aggregate(ndp.Aggregation(calculations=[total], group_by=["month"]))

	month_array = monthly_totals.column("month")
	month_list = month_array.to_list()
	total_array = monthly_totals.column("price_sum")
	total_list = total_array.to_list()
	assert month_list == EXPECTED_MONTHS
	assert total_list == EXPECTED_MONTH_TOTALS


def test_datetime_texts_without_format_keep_their_time_or_become_midnight() -> None:
	"""
	Check that texts with and without time are read as datetimes when no format is given.

	.. versionadded:: 0.1.0
	"""
	pickups = ndp.Array.from_list(PICKUP_TEXTS)
	trips = ndp.Table.from_arrays({"pickup": pickups})

	converted = trips.convert(ndp.TableConversion(column="pickup", dtype=ndp.Type.DATETIME))

	pickup_list = converted.column("pickup").to_list()
	assert pickup_list == EXPECTED_PICKUPS


def test_a_given_time_format_refuses_a_text_without_time() -> None:
	"""
	Check that a format given explicitly stays strict, and that the message cites the text and the format.

	.. versionadded:: 0.1.0
	"""
	pickups = ndp.Array.from_list([PICKUP_DAY])
	trips = ndp.Table.from_arrays({"pickup": pickups})
	conversion = ndp.TableConversion(
		column="pickup", dtype=ndp.Type.DATETIME, format=ndp.DateFormat.YEAR_MONTH_DAY_TIME
	)

	with pytest.raises(ndp.ValueConversionError, match="YEAR_MONTH_DAY_TIME") as caught_error:
		trips.convert(conversion)

	assert caught_error.value.rejected_value == PICKUP_DAY


def test_date_texts_with_a_time_are_refused_without_format() -> None:
	"""
	Check that reading a text with a time as a date is refused, since its time would be lost.

	.. versionadded:: 0.1.0
	"""
	pickups = ndp.Array.from_list([PICKUP_TIME])
	trips = ndp.Table.from_arrays({"pickup": pickups})

	with pytest.raises(ndp.ValueConversionError, match="YEAR_MONTH_DAY") as caught_error:
		trips.convert(ndp.TableConversion(column="pickup", dtype=ndp.Type.DATE))

	assert caught_error.value.rejected_value == PICKUP_TIME


@pytest.mark.parametrize("pickups", [MIDNIGHT_PICKUPS, VARIED_PICKUPS])
def test_datetimes_written_in_a_csv_file_are_read_back_without_format(tmp_path: Path, pickups: list[datetime]) -> None:
	"""
	Check that datetimes come back from a CSV file, whether every time is midnight or not.

	.. versionadded:: 0.1.0
	"""
	csv_path = tmp_path / TRIPS_CSV_NAME
	pickup_values = ndp.Array.from_list(pickups)
	trips = ndp.Table.from_arrays({"pickup": pickup_values})
	trips.to_csv(csv_path)

	read_trips = ndp.Table.from_csv(csv_path)
	converted = read_trips.convert(ndp.TableConversion(column="pickup", dtype=ndp.Type.DATETIME))

	pickup_list = converted.column("pickup").to_list()
	assert pickup_list == pickups


def test_a_time_format_on_dates_points_to_a_conversion_through_datetimes() -> None:
	"""
	Check that reading dates with a time format explains how to convert the column.

	.. versionadded:: 0.1.0
	"""
	trips = ndp.Table.from_arrays({"pickup": ndp.Array.from_list([PICKUP_TIME])})
	conversion = ndp.TableConversion(column="pickup", dtype=ndp.Type.DATE, format=ndp.DateFormat.YEAR_MONTH_DAY_TIME)

	with pytest.raises(ndp.InvalidConversionError, match=THROUGH_DATETIME_HINT):
		trips.convert(conversion)

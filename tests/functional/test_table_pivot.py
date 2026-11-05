"""
Functional tests of the pivot table of a Table.

.. versionadded:: 0.1.0
"""

from datetime import date

import pandas
import pytest

import numdaplot as ndp

TRIPS = ndp.Table.from_pandas(
	pandas.DataFrame(
		{
			"hour": [9.0, 8.0, 8.0, 9.0, 8.0],
			"color": pandas.Series(["green", "green", "yellow", "yellow", None], dtype="string"),
			"day": pandas.Series(["Tue", "Mon", "Tue", "Tue", "Mon"], dtype="string"),
			"fare": [1.0, 2.0, 3.0, None, 4.0],
		}
	)
)
EVERY_ROW = ndp.Calculation(column="fare", function=ndp.Count(missing=ndp.CountedMissing.INCLUDED))
TOTAL_FARE = ndp.Calculation(column="fare", function=ndp.Sum())
EXPECTED_NAMES = ["hour", "Mon", "Tue"]
EXPECTED_HOURS = [8.0, 9.0]
EXPECTED_MONDAY_ROWS = [2, 0]
EXPECTED_TUESDAY_ROWS = [1, 2]
EXPECTED_HOUR_NAMES = ["day", "8", "9"]
EXPECTED_MISSING_COLORS = [False, False, False, False, True]
EXPECTED_GROUPED_HOURS = [8.0, 9.0, 8.0, 9.0, 8.0]
EXPECTED_GROUPED_MONDAY = [2.0, 0.0, 0.0, 0.0, 4.0]
EXPECTED_MISSING_HINT = "drop_missing with ndp.MissingDrop"
EXPECTED_PRESENT_NAMES = ["hour", "green", "yellow"]
SALE_DAYS = [date(2026, 1, 5), date(2026, 1, 6)]
SALE_CITIES = ["Pau", "Pau"]
SALE_PRICES = [10.0, 20.0]
EXPECTED_DATE_NAMES = ["city", "2026-01-05", "2026-01-06"]


def test_a_pivot_table_gives_one_column_per_value() -> None:
	"""
	Check the rows and the columns of the result, and the count of each combination, 0 when it has no row.

	.. versionadded:: 0.1.0
	"""
	pivot = ndp.PivotTable(rows=["hour"], columns="day", calculation=EVERY_ROW)

	pivoted = TRIPS.pivot_table(pivot)

	assert pivoted.column_names == EXPECTED_NAMES
	assert pivoted.column("hour").to_list() == EXPECTED_HOURS
	assert pivoted.column("Mon").to_list() == EXPECTED_MONDAY_ROWS
	assert pivoted.column("Tue").to_list() == EXPECTED_TUESDAY_ROWS


def test_numbers_become_column_names_without_decimal_part() -> None:
	"""
	Check that the decimal hours name the columns as whole numbers.

	.. versionadded:: 0.1.0
	"""
	pivot = ndp.PivotTable(rows=["day"], columns="hour", calculation=EVERY_ROW)

	pivoted = TRIPS.pivot_table(pivot)

	assert pivoted.column_names == EXPECTED_HOUR_NAMES


def test_dates_become_column_names_year_first() -> None:
	"""
	Check that dates name the columns as written by a conversion to a text.

	.. versionadded:: 0.1.0
	"""
	days = ndp.Array.from_list(SALE_DAYS)
	cities = ndp.Array.from_list(SALE_CITIES)
	prices = ndp.Array.from_list(SALE_PRICES)
	sales = ndp.Table.from_arrays({"city": cities, "day": days, "price": prices})
	total = ndp.Calculation(column="price", function=ndp.Sum())

	pivoted = sales.pivot_table(ndp.PivotTable(rows=["city"], columns="day", calculation=total))

	assert pivoted.column_names == EXPECTED_DATE_NAMES


def test_several_row_columns_keep_the_missing_group_last() -> None:
	"""
	Check one row per combination of the row columns, the group of missing values being last.

	.. versionadded:: 0.1.0
	"""
	pivot = ndp.PivotTable(rows=["color", "hour"], columns="day", calculation=TOTAL_FARE)

	pivoted = TRIPS.pivot_table(pivot)

	missing_colors = pivoted.check(ndp.IsMissing()).column("color").to_list()
	assert missing_colors == EXPECTED_MISSING_COLORS
	assert pivoted.column("hour").to_list() == EXPECTED_GROUPED_HOURS
	assert pivoted.column("Mon").to_list() == EXPECTED_GROUPED_MONDAY


def test_a_column_holding_missing_values_is_refused_until_they_are_removed() -> None:
	"""
	Check the error pointing to drop_missing, and that following it works.

	.. versionadded:: 0.1.0
	"""
	pivot = ndp.PivotTable(rows=["hour"], columns="color", calculation=EVERY_ROW)

	with pytest.raises(ndp.RefusedOperationError, match=EXPECTED_MISSING_HINT):
		TRIPS.pivot_table(pivot)

	present_trips = TRIPS.drop_missing(ndp.MissingDrop(columns=["color"]))
	pivoted = present_trips.pivot_table(pivot)
	assert pivoted.column_names == EXPECTED_PRESENT_NAMES


def test_a_pivot_table_is_drawn_as_a_heatmap() -> None:
	"""
	Check that the result of a pivot table goes straight to plot_heatmap.

	.. versionadded:: 0.1.0
	"""
	pivoted = TRIPS.pivot_table(ndp.PivotTable(rows=["hour"], columns="day", calculation=EVERY_ROW))
	chart = ndp.HeatmapChart(columns=["Mon", "Tue"], labels="hour")

	plot = ndp.plot_heatmap(pivoted, chart)

	assert isinstance(plot, ndp.Plot)

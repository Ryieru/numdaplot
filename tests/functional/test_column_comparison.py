"""
Functional tests of the comparison of two columns, value by value.

.. versionadded:: 0.2.0
"""

from datetime import date, datetime

import pandas
import pytest

import numdaplot as ndp

REGIONS = ["N", "N", "S", "S"]
DEPARTURES = ["Pau", None, "Dax", "Nice"]
ARRIVALS = ["Pau", "Lyon", "Pau", "Nice"]
EXPECTED_ROUND_TRIP_CITIES = ["Pau", "Nice"]
EXPECTED_SAME_CITIES = [True, False, False, True]
PRICES = [10.0, 5.0, 9.0]
COSTS = [8.0, 7.0, 9.0]
EXPECTED_PROFITABLE_PRICES = [10.0]
EXPECTED_REGION_SHARES = [1.0, 0.5]
EXPECTED_SOUTH_NICE_SHARE = 1.0
SOUTH_REGION = "S"
CITY_NUMBERS = [1.0, 2.0, 3.0, 4.0]
EXPECTED_WHOLE_SHARE = 2 / 3
TRIP_GRID = [["Pau", "Dax", "Pau"], ["Nice", "Nice", "Lyon"]]
HOME_GRID = [["Pau", "Pau", "Pau"], ["Nice", "Dax", "Lyon"]]
EXPECTED_ROW_SHARES = [2 / 3, 2 / 3]
SHORT_ARRIVALS = ["Pau"]
EXPECTED_SHAPE_MESSAGE = "Expected matching shapes, got [4] and [1]."
EXPECTED_TYPE_MESSAGE = "Cannot apply Equal to the TEXT column 'departure' and FLOAT64."
VISIT_DAYS = [date(2026, 1, 1), date(2026, 1, 2)]
BOOKED_MOMENTS = [datetime(2026, 1, 1), datetime(2026, 1, 2, 9, 30)]
EXPECTED_SAME_MOMENTS = [True, False]
PICKUP_TEXTS = ["2026-03-14 23:30"]
PARIS_ZONE = "Europe/Paris"
EXPECTED_ZONE_MESSAGE = "A rule comparing a column with an Array needs datetimes without a time zone."
ROUND_TRIP_NAME = "round_trip"


def build_trips() -> ndp.Table:
	"""
	Return a Table of trips, with the city of departure and the city of arrival of each.

	.. versionadded:: 0.2.0

	Returns
	-------
	ndp.Table
		The columns region, departure and arrival.
	"""
	regions = ndp.Array.from_list(REGIONS)
	departures = ndp.Array.from_list(DEPARTURES)
	arrivals = ndp.Array.from_list(ARRIVALS)
	trips = ndp.Table.from_arrays({"region": regions, "departure": departures, "arrival": arrivals})

	return trips


def build_round_trip_share(trips: ndp.Table) -> ndp.Calculation:
	"""
	Return the calculation of the share of trips that end where they start.

	.. versionadded:: 0.2.0

	Parameters
	----------
	trips
		The Table of trips.

	Returns
	-------
	ndp.Calculation
		The share of departures equal to their arrival, named round_trip.
	"""
	arrivals = trips.column("arrival")
	same_city = ndp.Share(ndp.Equal(arrivals))
	round_trip_share = ndp.Calculation(column="departure", function=same_city, result_name=ROUND_TRIP_NAME)

	return round_trip_share


def test_rows_whose_two_columns_are_equal_are_kept() -> None:
	"""
	Check that a filter keeps the rows whose departure equals their arrival, a missing departure left out.

	.. versionadded:: 0.2.0
	"""
	trips = build_trips()
	arrivals = trips.column("arrival")
	condition = ndp.Condition(rule=ndp.Equal(arrivals), columns=["departure"])

	round_trips = trips.filter(ndp.Filter(conditions=[condition]))

	city_values = round_trips.column("departure")
	cities = city_values.to_list()
	assert cities == EXPECTED_ROUND_TRIP_CITIES


def test_two_arrays_are_compared_value_by_value() -> None:
	"""
	Check that check compares each text with the text at its position.

	.. versionadded:: 0.2.0
	"""
	trips = build_trips()
	departures = trips.column("departure")
	arrivals = trips.column("arrival")

	same_cities = departures.check(ndp.Equal(arrivals))

	same_city_list = same_cities.to_list()
	assert same_city_list == EXPECTED_SAME_CITIES


def test_values_greater_than_another_column_are_selected() -> None:
	"""
	Check that select keeps the prices above their cost.

	.. versionadded:: 0.2.0
	"""
	prices = ndp.Array.from_list(PRICES)
	costs = ndp.Array.from_list(COSTS)

	profitable_prices = prices.select(ndp.Greater(costs))

	profitable_list = profitable_prices.to_list()
	assert profitable_list == EXPECTED_PROFITABLE_PRICES


def test_a_share_comparing_two_columns_is_computed_for_each_group() -> None:
	"""
	Check that aggregate gives the share of round trips of each region.

	.. versionadded:: 0.2.0
	"""
	trips = build_trips()
	round_trip_share = build_round_trip_share(trips)

	shares = trips.aggregate(ndp.Aggregation(calculations=[round_trip_share], group_by=["region"]))

	share_values = shares.column(ROUND_TRIP_NAME)
	share_list = share_values.to_list()
	assert share_list == EXPECTED_REGION_SHARES


def test_a_share_comparing_two_columns_is_computed_in_a_pivot_table() -> None:
	"""
	Check that pivot_table gives the share of round trips of each region and city of arrival.

	.. versionadded:: 0.2.0
	"""
	trips = build_trips()
	arrivals = trips.column("arrival")
	same_city = ndp.Calculation(column="departure", function=ndp.Share(ndp.Equal(arrivals)))
	pivot = ndp.PivotTable(rows=["region"], columns="arrival", calculation=same_city)

	pivoted_shares = trips.pivot_table(pivot)

	nice_values = pivoted_shares.column("Nice")
	region_values = pivoted_shares.column("region")
	nice_shares = nice_values.to_list()
	regions = region_values.to_list()
	south_position = regions.index(SOUTH_REGION)
	assert nice_shares[south_position] == EXPECTED_SOUTH_NICE_SHARE


def test_a_share_comparing_two_columns_is_described() -> None:
	"""
	Check that describe gives the share of round trips of the departure column.

	.. versionadded:: 0.2.0
	"""
	trips = build_trips()
	arrivals = trips.column("arrival")
	description = ndp.Description(functions=[ndp.Share(ndp.Equal(arrivals))], columns=["departure"])

	described_trips = trips.describe(description)

	share_values = described_trips.column("departure")
	share = share_values.to_value()
	assert share == EXPECTED_WHOLE_SHARE


def test_a_share_comparing_two_grids_is_computed_for_each_row() -> None:
	"""
	Check that compute with an axis gives the share of each row of a grid compared with another grid.

	.. versionadded:: 0.2.0
	"""
	trips = ndp.Array.from_list(TRIP_GRID)
	homes = ndp.Array.from_list(HOME_GRID)

	row_shares = trips.compute(ndp.Share(ndp.Equal(homes)), axis=ndp.Axis.EACH_ROW)

	row_share_list = row_shares.to_list()
	assert row_share_list == EXPECTED_ROW_SHARES


def test_an_array_of_another_length_is_refused() -> None:
	"""
	Check that a filter comparing with an Array of another length raises ShapeMismatchError.

	.. versionadded:: 0.2.0
	"""
	trips = build_trips()
	short_arrivals = ndp.Array.from_list(SHORT_ARRIVALS)
	condition = ndp.Condition(rule=ndp.Equal(short_arrivals), columns=["departure"])

	with pytest.raises(ndp.ShapeMismatchError) as error_info:
		trips.filter(ndp.Filter(conditions=[condition]))

	error_text = str(error_info.value)
	assert error_text == EXPECTED_SHAPE_MESSAGE


def test_texts_compared_with_numbers_name_the_column() -> None:
	"""
	Check that a text column compared with numbers raises IncompatibleTypesError naming the column.

	.. versionadded:: 0.2.0
	"""
	trips = build_trips()
	numbers = ndp.Array.from_list(CITY_NUMBERS)
	condition = ndp.Condition(rule=ndp.Equal(numbers), columns=["departure"])

	with pytest.raises(ndp.IncompatibleTypesError) as error_info:
		trips.filter(ndp.Filter(conditions=[condition]))

	error_text = str(error_info.value)
	assert error_text == EXPECTED_TYPE_MESSAGE


def test_dates_equal_datetimes_at_midnight() -> None:
	"""
	Check that a date equals the datetime at midnight of that day, as with a single reference value.

	.. versionadded:: 0.2.0
	"""
	visit_days = ndp.Array.from_list(VISIT_DAYS)
	booked_moments = ndp.Array.from_list(BOOKED_MOMENTS)

	same_moments = visit_days.check(ndp.Equal(booked_moments))

	same_moment_list = same_moments.to_list()
	assert same_moment_list == EXPECTED_SAME_MOMENTS


def test_a_column_with_a_time_zone_is_refused() -> None:
	"""
	Check that a datetime column with a time zone compared with an Array raises TimeZoneMismatchError.

	.. versionadded:: 0.2.0
	"""
	naive_times = pandas.to_datetime(PICKUP_TEXTS)
	naive_column = pandas.Series(naive_times)
	zoned_column = naive_column.dt.tz_localize(PARIS_ZONE)
	rides = ndp.Table.from_pandas(pandas.DataFrame({"pickup": zoned_column}))
	moments = ndp.Array.from_list([datetime(2026, 3, 14, 22, 30)])
	condition = ndp.Condition(rule=ndp.Equal(moments), columns=["pickup"])

	with pytest.raises(ndp.TimeZoneMismatchError) as error_info:
		rides.filter(ndp.Filter(conditions=[condition]))

	error_text = str(error_info.value)
	assert error_text == EXPECTED_ZONE_MESSAGE

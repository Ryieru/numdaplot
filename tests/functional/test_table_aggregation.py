"""
Functional tests of the aggregation and the description of a Table.

.. versionadded:: 0.1.0
"""

from typing import Any

import pandas
import pytest

import numdaplot as ndp

SALES = pandas.DataFrame(
	{
		"city": pandas.Series(["Pau", "Lyon", None, "Pau", "Lyon"], dtype="string"),
		"price": [10.0, 30.0, 20.0, 50.0, None],
		"count": pandas.Series([1, 2, 3, None, 5], dtype="Int64"),
	}
)
EXPECTED_GROUP_NAMES = ["city", "price_mean", "count_sum", "price_quantile_97_5"]
EXPECTED_GROUP_CITIES = ["Lyon", "Pau", None]
EXPECTED_GROUP_MEANS = [30.0, 30.0, 20.0]
EXPECTED_GROUP_SUMS = [7, 1, 3]
HIGH_FRACTION = 0.975
EXPECTED_TOTAL_PRICE = 110.0
ONLY_LYON = ndp.Condition(rule=ndp.Equal("Lyon"), columns=["city"])
LYON_WITHOUT_PRICE = ndp.Condition(rule=ndp.IsMissing(), columns=["price"])
EXPECTED_DESCRIBED_NAMES = ["statistic", "price", "count"]
EXPECTED_STATISTICS = ["count", "mean", "standard_deviation", "min", "quantile_25", "median", "quantile_75", "max"]
EXPECTED_PRICE_COUNT = 4.0
EXPECTED_CITY_DESCRIPTION = ["4", "Lyon", None]


def build_sales() -> ndp.Table:
	"""
	Return a Table of five sales with holes in each column.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Table
		The sales.
	"""
	sales = ndp.Table.from_pandas(SALES)

	return sales


def read_values(table: ndp.Table, column_name: str) -> list[Any]:
	"""
	Return the values of a column with None for each missing value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	table
		Any Table.
	column_name
		The name of the column.

	Returns
	-------
	list[Any]
		The values.
	"""
	frame = table.to_pandas()
	column = frame[column_name]
	raw_values = column.tolist()
	missing = column.isna()
	missing_flags = missing.tolist()
	values = [None if is_missing else value for value, is_missing in zip(raw_values, missing_flags, strict=True)]

	return values


def test_groups_are_sorted_with_missing_values_last() -> None:
	"""
	Check the result names, the order of the groups and each statistic.

	.. versionadded:: 0.1.0
	"""
	sales = build_sales()
	average_price = ndp.Calculation(column="price", function=ndp.Mean())
	total_count = ndp.Calculation(column="count", function=ndp.Sum())
	high_price = ndp.Calculation(column="price", function=ndp.Quantile(HIGH_FRACTION))
	aggregation = ndp.Aggregation(calculations=[average_price, total_count, high_price], group_by=["city"])

	by_city = sales.aggregate(aggregation)

	cities = read_values(by_city, "city")
	means = read_values(by_city, "price_mean")
	sums = read_values(by_city, "count_sum")
	assert by_city.column_names == EXPECTED_GROUP_NAMES
	assert cities == EXPECTED_GROUP_CITIES
	assert means == EXPECTED_GROUP_MEANS
	assert sums == EXPECTED_GROUP_SUMS


def test_an_aggregation_without_group_gives_one_value() -> None:
	"""
	Check that the total price of every sale reads as a Python value.

	.. versionadded:: 0.1.0
	"""
	sales = build_sales()
	total_price = ndp.Calculation(column="price", function=ndp.Sum(), result_name="total")

	total = sales.aggregate(ndp.Aggregation(calculations=[total_price]))

	total_value = total.to_value()
	assert total_value == EXPECTED_TOTAL_PRICE


def test_a_group_without_present_value_gives_a_missing_mean() -> None:
	"""
	Check that the mean of no price is missing instead of an error.

	.. versionadded:: 0.1.0
	"""
	sales = build_sales()
	lyon_without_price = sales.filter(ndp.Filter(conditions=[ONLY_LYON, LYON_WITHOUT_PRICE]))
	average_price = ndp.Calculation(column="price", function=ndp.Mean())

	result = lyon_without_price.aggregate(ndp.Aggregation(calculations=[average_price], group_by=["city"]))

	means = read_values(result, "price_mean")
	assert means == [None]


def test_a_statistic_that_does_not_apply_to_its_column_is_refused() -> None:
	"""
	Check that the mean of cities raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	sales = build_sales()
	average_city = ndp.Calculation(column="city", function=ndp.Mean())

	with pytest.raises(ndp.IncompatibleTypesError):
		sales.aggregate(ndp.Aggregation(calculations=[average_city]))


def test_two_results_of_the_same_name_are_refused_at_creation() -> None:
	"""
	Check that two means of the price raise DuplicateColumnError.

	.. versionadded:: 0.1.0
	"""
	average_price = ndp.Calculation(column="price", function=ndp.Mean())

	with pytest.raises(ndp.DuplicateColumnError):
		ndp.Aggregation(calculations=[average_price, average_price])


def test_describe_gives_the_pandas_statistics_of_every_number_column() -> None:
	"""
	Check the described columns, the statistics, and the count of present prices.

	.. versionadded:: 0.1.0
	"""
	sales = build_sales()

	description = sales.describe(ndp.Description())

	statistics = read_values(description, "statistic")
	price_statistics = read_values(description, "price")
	assert description.column_names == EXPECTED_DESCRIBED_NAMES
	assert statistics == EXPECTED_STATISTICS
	assert price_statistics[0] == EXPECTED_PRICE_COUNT


def test_describe_writes_mixed_results_of_a_text_column_as_texts() -> None:
	"""
	Check the count, minimum and missing mean of the cities.

	.. versionadded:: 0.1.0
	"""
	sales = build_sales()
	functions = list[ndp.Statistic]([ndp.Count(), ndp.Min(), ndp.Mean()])

	description = sales.describe(ndp.Description(functions=functions, columns=["city"]))

	city_description = read_values(description, "city")
	assert city_description == EXPECTED_CITY_DESCRIPTION

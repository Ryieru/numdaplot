"""
Unit tests of the groups of rows, the result columns and the aggregation of a Table.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pandas
import pytest
from numpy.typing import NDArray

from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.statistics.count import Count
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.sum import Sum
from numdaplot.tables.aggregation.aggregated_frame import aggregate_frame, compute_group_results, take_group_keys
from numdaplot.tables.aggregation.aggregation import Aggregation
from numdaplot.tables.aggregation.calculation import Calculation
from numdaplot.tables.aggregation.result_column import build_result_column, compute_cell
from numdaplot.tables.aggregation.row_groups import find_row_groups

SALES = pandas.DataFrame(
	{
		"city": pandas.Series(["Pau", None, "Lyon", "Pau"], dtype="string"),
		"price": [10.0, 20.0, None, 30.0],
	}
)
EXPECTED_GROUPS = [[2], [0, 3], [1]]
EXPECTED_SINGLE_GROUP = [[0, 1, 2, 3]]
EMPTY_FRAME = pandas.DataFrame({"city": pandas.Series([], dtype="string")})
GROUP_ROWS = [numpy.array([2]), numpy.array([0, 3]), numpy.array([1])]
EXPECTED_KEYS = ["Lyon", "Pau", pandas.NA]
EXPECTED_GROUP_MEANS = [None, 20.0, 20.0]
EXPECTED_GROUP_COUNTS = [0, 2, 1]
EMPTY_DECIMALS = numpy.array([], dtype=numpy.float64)
TEXTS = numpy.array(["a"], dtype="T")
TWO_VALUES = numpy.array([2.0, 4.0])
EXPECTED_MEAN = [3.0]
EXPECTED_RESULTS = [2, pandas.NA]
EXPECTED_MISSING_RESULT_DTYPE = "float64"
EXPECTED_COLUMN_NAMES = ["city", "price_sum"]
EXPECTED_TOTALS = [0.0, 40.0, 20.0]
EXPECTED_TOTAL = [60.0]
TOTAL = Calculation(column="price", function=Sum())


def read_groups(groups: list[NDArray[Any]]) -> list[list[int]]:
	"""
	Return groups of rows as Python lists.

	.. versionadded:: 0.1.0

	Parameters
	----------
	groups
		The rows of each group.

	Returns
	-------
	list[list[int]]
		The rows of each group.
	"""
	group_lists = list[list[int]]()

	for group in groups:
		raw_rows = group.tolist()
		rows = cast(list[int], raw_rows)
		group_lists.append(rows)

	return group_lists


def read_with_none(values: list[Any]) -> list[Any]:
	"""
	Return values with None instead of NaN.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Any values.

	Returns
	-------
	list[Any]
		The values, NaN replaced with None.
	"""
	object_values = pandas.Series(values, dtype=object)
	missing = object_values.isna()
	missing_flags = missing.tolist()
	value_list = [None if is_missing else value for value, is_missing in zip(values, missing_flags, strict=True)]

	return value_list


def test_find_row_groups_sorts_the_groups_and_puts_missing_values_last() -> None:
	"""
	Check that Lyon comes before Pau and the missing city comes last.

	.. versionadded:: 0.1.0
	"""
	groups = find_row_groups(SALES, ["city"])

	group_lists = read_groups(groups)
	assert group_lists == EXPECTED_GROUPS


def test_find_row_groups_gives_a_single_group_without_group_column() -> None:
	"""
	Check that no group column gives every row in one group.

	.. versionadded:: 0.1.0
	"""
	groups = find_row_groups(SALES, None)

	group_lists = read_groups(groups)
	assert group_lists == EXPECTED_SINGLE_GROUP


def test_find_row_groups_gives_no_group_for_an_empty_table() -> None:
	"""
	Check that a Table without row has no group.

	.. versionadded:: 0.1.0
	"""
	groups = find_row_groups(EMPTY_FRAME, ["city"])

	assert groups == []


def test_take_group_keys_reads_the_first_row_of_each_group() -> None:
	"""
	Check the city of each group.

	.. versionadded:: 0.1.0
	"""
	key_columns = take_group_keys(SALES, ["city"], GROUP_ROWS)

	city_column = key_columns["city"]
	cities = city_column.tolist()
	assert cities == EXPECTED_KEYS


def test_compute_group_results_skips_the_missing_values_of_each_group() -> None:
	"""
	Check the mean of each group: a group without present value gives a missing mean.

	.. versionadded:: 0.1.0
	"""
	price_column = SALES["price"]

	result_column = compute_group_results(price_column, Mean(), GROUP_ROWS)

	result_values = result_column.tolist()
	means = read_with_none(result_values)
	assert means == EXPECTED_GROUP_MEANS


def test_compute_group_results_counts_zero_for_a_group_without_value() -> None:
	"""
	Check that Count gives 0 for a group without present value.

	.. versionadded:: 0.1.0
	"""
	price_column = SALES["price"]

	result_column = compute_group_results(price_column, Count(), GROUP_ROWS)

	counts = result_column.tolist()
	assert counts == EXPECTED_GROUP_COUNTS


def test_compute_cell_gives_nothing_when_a_value_is_needed() -> None:
	"""
	Check that the mean of no value gives None.

	.. versionadded:: 0.1.0
	"""
	result = compute_cell(EMPTY_DECIMALS, Mean())

	assert result is None


def test_compute_cell_gives_a_one_value_array() -> None:
	"""
	Check the mean of two values.

	.. versionadded:: 0.1.0
	"""
	result = compute_cell(TWO_VALUES, Mean())

	assert result is not None
	result_list = result.tolist()
	assert result_list == EXPECTED_MEAN


def test_compute_cell_rejects_a_statistic_that_does_not_apply() -> None:
	"""
	Check that the mean of texts raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		compute_cell(TEXTS, Mean())


def test_build_result_column_marks_missing_results() -> None:
	"""
	Check that None becomes a missing value.

	.. versionadded:: 0.1.0
	"""
	result_column = build_result_column([numpy.array([2]), None])

	results = result_column.tolist()
	assert results == EXPECTED_RESULTS


def test_build_result_column_uses_decimals_without_any_result() -> None:
	"""
	Check that only missing results give a FLOAT64 column.

	.. versionadded:: 0.1.0
	"""
	result_column = build_result_column([None])

	dtype_name = str(result_column.dtype)
	assert dtype_name == EXPECTED_MISSING_RESULT_DTYPE


def test_aggregate_frame_puts_the_group_columns_first() -> None:
	"""
	Check the column names and the sums of each city.

	.. versionadded:: 0.1.0
	"""
	aggregation = Aggregation(calculations=[TOTAL], group_by=["city"])

	aggregated_frame = aggregate_frame(SALES, aggregation)

	column_names = aggregated_frame.columns.tolist()
	total_column = aggregated_frame["price_sum"]
	totals = total_column.tolist()
	assert column_names == EXPECTED_COLUMN_NAMES
	assert totals == EXPECTED_TOTALS


def test_aggregate_frame_gives_one_row_without_group() -> None:
	"""
	Check the sum of the whole Table.

	.. versionadded:: 0.1.0
	"""
	aggregation = Aggregation(calculations=[TOTAL])

	aggregated_frame = aggregate_frame(SALES, aggregation)

	total_column = aggregated_frame["price_sum"]
	totals = total_column.tolist()
	assert totals == EXPECTED_TOTAL


@pytest.mark.parametrize(
	"aggregation",
	[
		Aggregation(calculations=[Calculation(column="prise", function=Sum())]),
		Aggregation(calculations=[TOTAL], group_by=["town"]),
	],
)
def test_aggregate_frame_rejects_an_unknown_column(aggregation: Aggregation) -> None:
	"""
	Check that an unknown calculation or group column raises ColumnNotFoundError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	aggregation
		An aggregation naming an unknown column.
	"""
	with pytest.raises(ColumnNotFoundError):
		aggregate_frame(SALES, aggregation)

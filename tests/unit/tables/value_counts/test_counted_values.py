"""
Unit tests of the count of the values of a column of a Table.

.. versionadded:: 0.2.0
"""

import numpy
import pandas
import pytest

from numdaplot.column_storage.column_values import find_column_type
from numdaplot.errors.tables.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.tables.duplicate_column_error import DuplicateColumnError
from numdaplot.measures.measure import Measure
from numdaplot.tables.value_counts.counted_values import count_frame_values, measure_groups, order_by_size
from numdaplot.tables.value_counts.value_count import ValueCount
from numdaplot.types.type import Type

CODE_COLUMN = "code"
COUNT_NAME = "value_count"
RATIO_NAME = "value_ratio"
UNKNOWN_COLUMN = "age"
FRAME = pandas.DataFrame({CODE_COLUMN: pandas.Series([7, None, 3, 7, 9], dtype="Int64")})
EXPECTED_PRESENT_CODES = [7, 3, 9]
EXPECTED_MISSING_CODES = [False, False, False, True]
EXPECTED_COUNTS = [2, 1, 1, 1]
EXPECTED_RATIOS = [0.4, 0.2, 0.2, 0.2]
EXPECTED_NAMES = [CODE_COLUMN, COUNT_NAME]
EMPTY_FRAME = pandas.DataFrame({CODE_COLUMN: pandas.Series(dtype="float64")})
NAMED_LIKE_COUNT_FRAME = pandas.DataFrame({COUNT_NAME: [1.0, 2.0]})
GROUP_SIZES = numpy.array([1, 3, 1, 5], dtype=numpy.int64)
EXPECTED_ORDER_WITH_MISSING_GROUP = [1, 0, 2, 3]
EXPECTED_ORDER_WITHOUT_MISSING_GROUP = [3, 1, 0, 2]
NO_GROUP_SIZES = numpy.array([], dtype=numpy.int64)
WEIGHT_COLUMN = "weight"
WEIGHTED_COUNT_NAME = "weighted_count"
WEIGHTED_RATIO_NAME = "weighted_ratio"
WEIGHTED_FRAME = pandas.DataFrame(
	{
		CODE_COLUMN: pandas.Series([2, 1, 2, 9], dtype="Int64"),
		WEIGHT_COLUMN: [100.0, 300.0, 100.0, None],
	}
)
EXPECTED_WEIGHTED_CODES = [1, 2]
EXPECTED_WEIGHTED_NAMES = [CODE_COLUMN, WEIGHTED_COUNT_NAME]
EXPECTED_WEIGHTED_COUNTS = [300.0, 200.0]
EXPECTED_WEIGHTED_RATIOS = [0.6, 0.4]
ZERO_WEIGHT_FRAME = pandas.DataFrame({CODE_COLUMN: [1, 2], WEIGHT_COLUMN: [0.0, 0.0]})
ROW_GROUPS = [numpy.array([0, 2]), numpy.array([1])]
GROUP_WEIGHTS = numpy.array([100.0, 300.0, 50.0])
EXPECTED_GROUP_SIZES = [2, 1]
EXPECTED_GROUP_WEIGHTS = [150.0, 300.0]


def test_count_frame_values_goes_from_the_most_frequent_value_to_the_missing_value() -> None:
	"""
	Check the order of the values: by count, then by value, the missing value last.

	.. versionadded:: 0.2.0
	"""
	counted_frame = count_frame_values(FRAME, ValueCount(column=CODE_COLUMN))

	code_column = counted_frame[CODE_COLUMN]
	missing_codes = code_column.isna()
	present_codes = code_column.dropna()
	missing_list = missing_codes.tolist()
	present_list = present_codes.tolist()
	assert missing_list == EXPECTED_MISSING_CODES
	assert present_list == EXPECTED_PRESENT_CODES


def test_count_frame_values_counts_the_rows_of_each_value() -> None:
	"""
	Check the counts and the names of the columns.

	.. versionadded:: 0.2.0
	"""
	counted_frame = count_frame_values(FRAME, ValueCount(column=CODE_COLUMN))

	count_column = counted_frame[COUNT_NAME]
	count_list = count_column.tolist()
	column_names = counted_frame.columns.tolist()
	assert count_list == EXPECTED_COUNTS
	assert column_names == EXPECTED_NAMES


def test_count_frame_values_keeps_the_type_of_the_counted_column() -> None:
	"""
	Check that integer codes stay integers, and that the counts are integers.

	.. versionadded:: 0.2.0
	"""
	counted_frame = count_frame_values(FRAME, ValueCount(column=CODE_COLUMN))

	code_column = counted_frame[CODE_COLUMN]
	count_column = counted_frame[COUNT_NAME]
	code_type = find_column_type(code_column)
	count_type = find_column_type(count_column)
	assert code_type == Type.INT64
	assert count_type == Type.INT64


def test_count_frame_values_divides_by_every_row() -> None:
	"""
	Check that the ratios count the missing values in their total.

	.. versionadded:: 0.2.0
	"""
	ratio_count = ValueCount(column=CODE_COLUMN, measure=Measure.RATIO)

	counted_frame = count_frame_values(FRAME, ratio_count)

	ratio_column = counted_frame[RATIO_NAME]
	ratio_list = ratio_column.tolist()
	assert ratio_list == EXPECTED_RATIOS


def test_count_frame_values_gives_no_row_for_an_empty_table() -> None:
	"""
	Check that a Table without rows gives an empty count instead of an error.

	.. versionadded:: 0.2.0
	"""
	ratio_count = ValueCount(column=CODE_COLUMN, measure=Measure.RATIO)

	counted_frame = count_frame_values(EMPTY_FRAME, ratio_count)

	row_count = len(counted_frame)
	assert row_count == 0


def test_count_frame_values_rejects_an_unknown_column() -> None:
	"""
	Check that a column the Table does not have raises ColumnNotFoundError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(ColumnNotFoundError):
		count_frame_values(FRAME, ValueCount(column=UNKNOWN_COLUMN))


def test_count_frame_values_rejects_a_column_named_like_the_measure() -> None:
	"""
	Check that counting a column named ``value_count`` raises DuplicateColumnError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(DuplicateColumnError):
		count_frame_values(NAMED_LIKE_COUNT_FRAME, ValueCount(column=COUNT_NAME))


def test_order_by_size_keeps_the_missing_group_last() -> None:
	"""
	Check that the last group stays last when it holds the missing value, and that ties keep their order.

	.. versionadded:: 0.2.0
	"""
	group_order = order_by_size(GROUP_SIZES, True)

	order_list = group_order.tolist()
	assert order_list == EXPECTED_ORDER_WITH_MISSING_GROUP


def test_order_by_size_sorts_every_group_without_missing_group() -> None:
	"""
	Check that every group is sorted by size when none holds the missing value.

	.. versionadded:: 0.2.0
	"""
	group_order = order_by_size(GROUP_SIZES, False)

	order_list = group_order.tolist()
	assert order_list == EXPECTED_ORDER_WITHOUT_MISSING_GROUP


def test_order_by_size_gives_no_group_without_group() -> None:
	"""
	Check that no group gives an empty order.

	.. versionadded:: 0.2.0
	"""
	group_order = order_by_size(NO_GROUP_SIZES, False)

	group_count = len(group_order)
	assert group_count == 0


def test_count_frame_values_sums_the_weights_of_each_value() -> None:
	"""
	Check that weights give the sum of the weights of each value, the largest first, rows without weight left out.

	.. versionadded:: 0.2.0
	"""
	value_count = ValueCount(column=CODE_COLUMN, weights=WEIGHT_COLUMN)

	counted_frame = count_frame_values(WEIGHTED_FRAME, value_count)

	column_names = counted_frame.columns.tolist()
	code_column = counted_frame[CODE_COLUMN]
	count_column = counted_frame[WEIGHTED_COUNT_NAME]
	codes = code_column.tolist()
	weighted_counts = count_column.tolist()
	assert column_names == EXPECTED_WEIGHTED_NAMES
	assert codes == EXPECTED_WEIGHTED_CODES
	assert weighted_counts == EXPECTED_WEIGHTED_COUNTS


def test_count_frame_values_divides_by_the_sum_of_the_weights() -> None:
	"""
	Check that weighted ratios divide by the sum of the weights of the rows that count.

	.. versionadded:: 0.2.0
	"""
	value_count = ValueCount(column=CODE_COLUMN, measure=Measure.RATIO, weights=WEIGHT_COLUMN)

	counted_frame = count_frame_values(WEIGHTED_FRAME, value_count)

	ratio_column = counted_frame[WEIGHTED_RATIO_NAME]
	weighted_ratios = ratio_column.tolist()
	assert weighted_ratios == EXPECTED_WEIGHTED_RATIOS


def test_count_frame_values_gives_no_ratio_when_every_weight_is_zero() -> None:
	"""
	Check that weights summing to 0 give missing ratios.

	.. versionadded:: 0.2.0
	"""
	value_count = ValueCount(column=CODE_COLUMN, measure=Measure.RATIO, weights=WEIGHT_COLUMN)

	counted_frame = count_frame_values(ZERO_WEIGHT_FRAME, value_count)

	ratio_column = counted_frame[WEIGHTED_RATIO_NAME]
	missing_ratios = ratio_column.isna()
	all_missing = bool(missing_ratios.all())
	assert all_missing


def test_measure_groups_counts_the_rows_without_weights() -> None:
	"""
	Check that each group measures its number of rows without weights.

	.. versionadded:: 0.2.0
	"""
	group_sizes = measure_groups(ROW_GROUPS, None)

	size_list = group_sizes.tolist()
	assert size_list == EXPECTED_GROUP_SIZES


def test_measure_groups_sums_the_weights_of_each_group() -> None:
	"""
	Check that each group measures the sum of the weights of its rows.

	.. versionadded:: 0.2.0
	"""
	group_sizes = measure_groups(ROW_GROUPS, GROUP_WEIGHTS)

	size_list = group_sizes.tolist()
	assert size_list == EXPECTED_GROUP_WEIGHTS

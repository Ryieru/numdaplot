"""
Count of the values of a column of a Table.

.. versionadded:: 0.2.0
"""

from typing import Any, cast

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.argument_checks.column_names import require_known_columns
from numdaplot.column_storage.column import Column
from numdaplot.column_storage.column_values import build_column, find_column_missing
from numdaplot.errors.tables.duplicate_column_error import DuplicateColumnError
from numdaplot.measures.count_division import divide_counts
from numdaplot.measures.measure import Measure
from numdaplot.tables.aggregation.aggregated_frame import take_group_keys
from numdaplot.tables.aggregation.row_groups import STABLE_SORT, find_row_groups, measure_group_sizes
from numdaplot.tables.value_counts.row_weights import select_weighted_rows
from numdaplot.tables.value_counts.value_count import ValueCount

MEASURE_COLUMN_NAMES = {
	Measure.COUNT: "value_count",
	Measure.RATIO: "value_ratio",
}
WEIGHTED_MEASURE_COLUMN_NAMES = {
	Measure.COUNT: "weighted_count",
	Measure.RATIO: "weighted_ratio",
}


def count_frame_values(frame: pandas.DataFrame, value_count: ValueCount) -> pandas.DataFrame:
	"""
	Return how many rows hold each value of a column, from the most frequent value to the least frequent.

	With weights, each value counts the sum of the weights of its rows, the rows without weight left out.

	.. versionadded:: 0.2.0

	Parameters
	----------
	frame
		The columns of a Table.
	value_count
		The counted column, the measure and the column of weights.

	Returns
	-------
	pandas.DataFrame
		The counted column holding each value once, then a ``value_count`` or ``value_ratio`` column, or with weights
		a ``weighted_count`` or ``weighted_ratio`` column. Values with the same count are sorted by value, and the
		missing value comes last when there is one.

	Raises
	------
	ColumnNotFoundError
		When the counted column or the column of weights does not exist.
	DuplicateColumnError
		When the counted column has the name of the measure column.
	IncompatibleTypesError
		When the column of weights does not hold numbers.
	InvalidWeightError
		When a weight is negative.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.value_counts.counted_values import count_frame_values
	>>> frame = pandas.DataFrame({"city": ["Pau", "Lyon", "Pau"]})
	>>> count_frame_values(frame, ndp.ValueCount(column="city"))
	   city  value_count
	0   Pau            2
	1  Lyon            1
	"""
	column_names = [str(column_name) for column_name in frame.columns]
	require_known_columns([value_count.column], column_names)
	measure_names = MEASURE_COLUMN_NAMES if value_count.weights is None else WEIGHTED_MEASURE_COLUMN_NAMES
	measure_name = measure_names[value_count.measure]
	if value_count.column == measure_name:
		raise DuplicateColumnError(measure_name)

	weighted_rows = select_weighted_rows(frame, value_count.weights)
	counted_frame_rows = weighted_rows.frame
	counted_column = counted_frame_rows[value_count.column]
	row_groups = find_row_groups(counted_frame_rows, [value_count.column])
	group_sizes = measure_groups(row_groups, weighted_rows.weights)
	missing = find_column_missing(counted_column)
	has_missing_group = bool(missing.any())
	group_order = order_by_size(group_sizes, has_missing_group)
	# Some versions of numpy type the list of tolist as unknown.
	group_numbers = cast(list[int], group_order.tolist())
	ordered_groups = list[NDArray[Any]]()

	for group_number in group_numbers:
		row_group = row_groups[group_number]
		ordered_groups.append(row_group)

	value_columns = take_group_keys(counted_frame_rows, [value_count.column], ordered_groups)
	ordered_sizes = group_sizes[group_order]
	measures = ordered_sizes
	if value_count.measure == Measure.RATIO:
		total_size = float(group_sizes.sum())
		measures = divide_counts(ordered_sizes, total_size)

	measure_column = build_column(measures)
	result_columns = dict[str, Column](value_columns)
	result_columns[measure_name] = measure_column
	counted_frame = pandas.DataFrame(result_columns)

	return counted_frame


def measure_groups(
	row_groups: list[NDArray[Any]], weights: NDArray[numpy.float64] | None
) -> NDArray[numpy.int64] | NDArray[numpy.float64]:
	"""
	Return the size of each group of rows: its number of rows, or the sum of their weights.

	.. versionadded:: 0.2.0

	Parameters
	----------
	row_groups
		The rows of each group.
	weights
		The weight of each row, or None when every row counts once.

	Returns
	-------
	NDArray[numpy.int64] or NDArray[numpy.float64]
		The number of rows of each group without weights, the decimal sum of their weights otherwise.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.value_counts.counted_values import measure_groups
	>>> row_groups = [numpy.array([0, 2]), numpy.array([1])]
	>>> measure_groups(row_groups, None)
	array([2, 1])
	>>> measure_groups(row_groups, numpy.array([100.0, 300.0, 100.0]))
	array([200., 300.])
	"""
	if weights is None:
		group_sizes = measure_group_sizes(row_groups)
		return group_sizes

	weight_sums = list[float]()

	for row_group in row_groups:
		group_weights = weights[row_group]
		weight_sum = float(group_weights.sum())
		weight_sums.append(weight_sum)

	weighted_sizes = numpy.array(weight_sums, dtype=numpy.float64)

	return weighted_sizes


def order_by_size(
	group_sizes: NDArray[numpy.int64] | NDArray[numpy.float64], has_missing_group: bool
) -> NDArray[numpy.intp]:
	"""
	Return the order of the groups from the largest to the smallest, the group of the missing value kept last.

	.. versionadded:: 0.2.0

	Parameters
	----------
	group_sizes
		The number of rows or the sum of the weights of each group, groups sorted by value with the group of the
		missing value last.
	has_missing_group
		Whether the last group is the group of the missing value.

	Returns
	-------
	NDArray[numpy.intp]
		The group numbers in their new order. Groups of the same size keep their order by value.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.value_counts.counted_values import order_by_size
	>>> order_by_size(numpy.array([1, 3, 1, 5]), True)
	array([1, 0, 2, 3])
	"""
	group_count = len(group_sizes)
	value_group_count = group_count
	if has_missing_group:
		value_group_count = group_count - 1

	value_group_sizes = group_sizes[:value_group_count]
	negated_sizes = -value_group_sizes
	value_group_order = numpy.argsort(negated_sizes, kind=STABLE_SORT)
	missing_group_numbers = numpy.arange(value_group_count, group_count)
	group_order = numpy.concatenate([value_group_order, missing_group_numbers])

	return group_order

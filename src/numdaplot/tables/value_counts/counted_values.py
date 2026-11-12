"""
Count of the values of a column of a Table.

.. versionadded:: 0.2.0
"""

from typing import Any, cast

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.ratios.count_division import divide_counts
from numdaplot.ratios.measure import Measure
from numdaplot.tables.aggregation.aggregated_frame import take_group_keys
from numdaplot.tables.aggregation.row_groups import STABLE_SORT, find_row_groups, measure_group_sizes
from numdaplot.tables.columns.column_names import require_known_columns
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import build_column, find_column_missing
from numdaplot.tables.value_counts.value_count import ValueCount

MEASURE_COLUMN_NAMES = {
	Measure.COUNT: "value_count",
	Measure.RATIO: "value_ratio",
}


def count_frame_values(frame: pandas.DataFrame, value_count: ValueCount) -> pandas.DataFrame:
	"""
	Return how many rows hold each value of a column, from the most frequent value to the least frequent.

	.. versionadded:: 0.2.0

	Parameters
	----------
	frame
		The columns of a Table.
	value_count
		The counted column and the measure.

	Returns
	-------
	pandas.DataFrame
		The counted column holding each value once, then a ``value_count`` or ``value_ratio`` column.
		Values with the same count are sorted by value, and the missing value comes last when there is one.

	Raises
	------
	ColumnNotFoundError
		When the counted column does not exist.
	DuplicateColumnError
		When the counted column has the name of the measure column.

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
	measure_name = MEASURE_COLUMN_NAMES[value_count.measure]
	if value_count.column == measure_name:
		raise DuplicateColumnError(measure_name)

	counted_column = frame[value_count.column]
	row_groups = find_row_groups(frame, [value_count.column])
	group_sizes = measure_group_sizes(row_groups)
	missing = find_column_missing(counted_column)
	has_missing_group = bool(missing.any())
	group_order = order_by_size(group_sizes, has_missing_group)
	# Some versions of numpy type the list of tolist as unknown.
	group_numbers = cast(list[int], group_order.tolist())
	ordered_groups = list[NDArray[Any]]()

	for group_number in group_numbers:
		row_group = row_groups[group_number]
		ordered_groups.append(row_group)

	value_columns = take_group_keys(frame, [value_count.column], ordered_groups)
	ordered_sizes = group_sizes[group_order]
	measures = ordered_sizes
	if value_count.measure == Measure.RATIO:
		row_count = len(frame)
		measures = divide_counts(ordered_sizes, row_count)

	measure_column = build_column(measures)
	result_columns = dict[str, Column](value_columns)
	result_columns[measure_name] = measure_column
	counted_frame = pandas.DataFrame(result_columns)

	return counted_frame


def order_by_size(group_sizes: NDArray[numpy.int64], has_missing_group: bool) -> NDArray[numpy.intp]:
	"""
	Return the order of the groups from the largest to the smallest, the group of the missing value kept last.

	.. versionadded:: 0.2.0

	Parameters
	----------
	group_sizes
		The number of rows of each group, groups sorted by value with the group of the missing value last.
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

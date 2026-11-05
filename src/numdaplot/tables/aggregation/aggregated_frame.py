"""
Aggregation of the rows of a Table.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.statistics.statistic import Statistic
from numdaplot.tables.aggregation.aggregation import Aggregation
from numdaplot.tables.aggregation.calculation import find_result_name
from numdaplot.tables.aggregation.result_column import build_result_column, compute_cell
from numdaplot.tables.aggregation.row_groups import find_row_groups
from numdaplot.tables.columns.column_names import require_known_columns
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_missing, read_present_values
from numdaplot.tables.frames.named_column_errors import NamedColumnErrors
from numdaplot.tables.frames.time_zones import attribute_source_time_zone

FIRST_ROW = 0
ROW_POSITION_DTYPE = numpy.int64


def aggregate_frame(frame: pandas.DataFrame, aggregation: Aggregation) -> pandas.DataFrame:
	"""
	Return the statistics of the whole Table, or of each group of rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	aggregation
		The statistics and the group columns.

	Returns
	-------
	pandas.DataFrame
		One row per group, sorted by group values with missing values last, or a single row.
		The group columns come first, then one column per calculation.

	Raises
	------
	ColumnNotFoundError
		When a calculation or a group names a column the Table does not have.
	IncompatibleTypesError
		When a statistic does not apply to the type of its column.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.aggregation.aggregated_frame import aggregate_frame
	>>> frame = pandas.DataFrame({"city": ["Pau", "Lyon", "Pau"], "price": [1.0, 2.0, 3.0]})
	>>> total = ndp.Calculation(column="price", function=ndp.Sum())
	>>> aggregate_frame(frame, ndp.Aggregation(calculations=[total], group_by=["city"]))
	   city  price_sum
	0  Lyon        2.0
	1   Pau        4.0
	"""
	column_names = [str(column_name) for column_name in frame.columns]
	calculation_columns = [calculation.column for calculation in aggregation.calculations]
	require_known_columns(calculation_columns, column_names)
	group_by = aggregation.group_by
	if group_by is not None:
		require_known_columns(group_by, column_names)

	row_groups = find_row_groups(frame, group_by)
	result_columns = dict[str, Column]()
	if group_by is not None:
		key_columns = take_group_keys(frame, group_by, row_groups)
		result_columns.update(key_columns)

	for calculation in aggregation.calculations:
		result_name = find_result_name(calculation)
		column = frame[calculation.column]
		result_column = compute_group_results(column, calculation.function, row_groups)
		result_columns[result_name] = result_column

	group_count = len(row_groups)
	group_numbers = pandas.RangeIndex(group_count)
	aggregated_frame = pandas.DataFrame(result_columns, index=group_numbers)

	return aggregated_frame


def take_group_keys(frame: pandas.DataFrame, group_by: list[str], row_groups: list[NDArray[Any]]) -> dict[str, Column]:
	"""
	Return the values of the group columns for each group, taken from its first row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	group_by
		The names of the group columns.
	row_groups
		The rows of each group.

	Returns
	-------
	dict[str, Column]
		One column per group column, one row per group, numbered from 0.

	Examples
	--------
	>>> import numpy
	>>> import pandas
	>>> from numdaplot.tables.aggregation.aggregated_frame import take_group_keys
	>>> frame = pandas.DataFrame({"city": ["Pau", "Lyon", "Pau"]})
	>>> take_group_keys(frame, ["city"], [numpy.array([1]), numpy.array([0, 2])])["city"].tolist()
	['Lyon', 'Pau']
	"""
	first_row_list = [row_group[FIRST_ROW] for row_group in row_groups]
	first_rows = numpy.array(first_row_list, dtype=ROW_POSITION_DTYPE)
	key_columns = dict[str, Column]()

	for column_name in group_by:
		column = frame[column_name]
		first_values = column.iloc[first_rows]
		key_column = first_values.reset_index(drop=True)
		key_columns[column_name] = key_column

	return key_columns


def compute_group_results(column: Column, statistic: Statistic, row_groups: list[NDArray[Any]]) -> Column:
	"""
	Return a statistic of the values of a column, for each group of rows, missing values left out unless counted.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column.
	statistic
		Any statistic of numdaplot.
	row_groups
		The rows of each group.

	Returns
	-------
	Column
		One result per group, missing for a group without present value when the statistic needs one.

	Raises
	------
	IncompatibleTypesError
		When the statistic does not apply to the type of the column.

	Examples
	--------
	>>> import numpy
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.aggregation.aggregated_frame import compute_group_results
	>>> column = pandas.Series([1.0, None, 3.0])
	>>> compute_group_results(column, ndp.Mean(), [numpy.array([1]), numpy.array([0, 2])]).tolist()
	[nan, 2.0]
	"""
	missing = find_column_missing(column)
	present = ~missing
	present_values = read_present_values(column)
	present_counts = numpy.cumsum(present)
	value_positions = present_counts - 1
	results = list[NDArray[Any] | None]()

	with NamedColumnErrors(column):
		for row_group in row_groups:
			group_present = present[row_group]
			present_rows = row_group[group_present]
			group_value_positions = value_positions[present_rows]
			group_values = present_values[group_value_positions]
			group_size = len(row_group)
			result = compute_cell(group_values, statistic, group_size)
			results.append(result)

	utc_results = build_result_column(results)
	result_column = attribute_source_time_zone(utc_results, column)

	return result_column

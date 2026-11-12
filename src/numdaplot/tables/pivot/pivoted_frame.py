"""
Pivot table of the rows of a Table.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.data_types.number_types import DECIMAL_TYPES
from numdaplot.data_types.type import Type
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.tables.aggregation.aggregated_frame import compute_group_results, take_group_keys
from numdaplot.tables.aggregation.row_groups import find_row_groups, split_positions
from numdaplot.tables.columns.column_names import require_known_columns, require_unique_names
from numdaplot.tables.columns.converted_column import convert_column
from numdaplot.tables.columns.table_conversion import TableConversion
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_missing, find_column_type
from numdaplot.tables.pivot.pivot_table import PivotTable

MISSING_PIVOT_OPERATION = "Pivoting the column {column_name!r} while it holds missing values"
MISSING_PIVOT_ALTERNATIVE = "drop_missing with ndp.MissingDrop(columns=[{column_name!r}])"
FIRST_ROW = 0
ROW_POSITION_DTYPE = numpy.int64


def pivot_frame(frame: pandas.DataFrame, pivot: PivotTable) -> pandas.DataFrame:
	"""
	Return one row per group of rows and one column per value of a column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	pivot
		The columns forming the rows and the columns of the result, and the statistic of each cell.

	Returns
	-------
	pandas.DataFrame
		The columns of ``rows``, then one column per value of ``columns``, both sorted.

	Raises
	------
	ColumnNotFoundError
		When a setting names a column the Table does not have.
	RefusedOperationError
		When the column of ``columns`` holds missing values.
	DuplicateColumnError
		When a value written as a text is also the name of a column of ``rows``.
	IncompatibleTypesError
		When the statistic does not apply to the type of its column.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.pivot.pivoted_frame import pivot_frame
	>>> days = pandas.Series(["Mon", "Tue", "Mon"], dtype="string")
	>>> frame = pandas.DataFrame({"hour": [8, 8, 9], "day": days, "fare": [7.0, 9.0, 5.0]})
	>>> total = ndp.Calculation(column="fare", function=ndp.Sum())
	>>> pivot_frame(frame, ndp.PivotTable(rows=["hour"], columns="day", calculation=total))
	   hour  Mon  Tue
	0     8  7.0  9.0
	1     9  5.0  0.0
	"""
	column_names = [str(column_name) for column_name in frame.columns]
	calculation = pivot.calculation
	requested_names = [*pivot.rows, pivot.columns, calculation.column]
	require_known_columns(requested_names, column_names)
	pivot_column = frame[pivot.columns]
	require_present_pivot_values(pivot_column, pivot.columns)
	row_groups = find_row_groups(frame, pivot.rows)
	column_groups = find_row_groups(frame, [pivot.columns])
	value_names = name_value_columns(pivot_column, column_groups, pivot.columns)
	output_names = [*pivot.rows, *value_names]
	require_unique_names(output_names)
	row_count = len(frame)
	group_numbers = number_row_groups(row_groups, row_count)
	group_count = len(row_groups)
	result_columns = take_group_keys(frame, pivot.rows, row_groups)
	value_column = frame[calculation.column]

	for value_name, column_rows in zip(value_names, column_groups, strict=True):
		column_group_numbers = group_numbers[column_rows]
		cell_rows = split_positions(column_rows, column_group_numbers, group_count)
		result_columns[value_name] = compute_group_results(value_column, calculation.function, cell_rows)

	result_numbers = pandas.RangeIndex(group_count)
	pivoted_frame = pandas.DataFrame(result_columns, index=result_numbers)

	return pivoted_frame


def require_present_pivot_values(pivot_column: Column, column_name: str) -> None:
	"""
	Check that the column giving its values to the result columns holds no missing value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	pivot_column
		The column.
	column_name
		Its name.

	Raises
	------
	RefusedOperationError
		When the column holds a missing value, which could not name a result column.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.pivot.pivoted_frame import require_present_pivot_values
	>>> try:
	... 	require_present_pivot_values(pandas.Series(["Mon", None], dtype="string"), "day")
	... except ndp.RefusedOperationError as error:
	... 	print(error)
	Pivoting the column 'day' while it holds missing values is not available,
	use drop_missing with ndp.MissingDrop(columns=['day']) instead.
	"""
	missing = find_column_missing(pivot_column)
	has_missing = bool(missing.any())
	if has_missing:
		operation = MISSING_PIVOT_OPERATION.format(column_name=column_name)
		alternative = MISSING_PIVOT_ALTERNATIVE.format(column_name=column_name)
		raise RefusedOperationError(operation, alternative)


def name_value_columns(pivot_column: Column, column_groups: list[NDArray[Any]], column_name: str) -> list[str]:
	"""
	Return the name of the result column of each value, the value written as a text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	pivot_column
		The column giving its values to the result columns.
	column_groups
		The rows of each value.
	column_name
		The name of the column.

	Returns
	-------
	list[str]
		One name per group. A whole decimal is written without decimal part.

	Examples
	--------
	>>> import numpy
	>>> import pandas
	>>> from numdaplot.tables.pivot.pivoted_frame import name_value_columns
	>>> name_value_columns(pandas.Series([1.0, 2.5]), [numpy.array([0]), numpy.array([1])], "hour")
	['1', '2.5']
	"""
	first_row_list = [column_group[FIRST_ROW] for column_group in column_groups]
	first_rows = numpy.array(first_row_list, dtype=ROW_POSITION_DTYPE)
	first_values = pivot_column.iloc[first_rows]
	source_type = find_column_type(pivot_column)
	if source_type in DECIMAL_TYPES:
		decimals = cast(list[float], first_values.tolist())
		decimal_names = [write_decimal(decimal) for decimal in decimals]
		return decimal_names

	text_conversion = TableConversion(column=column_name, dtype=Type.TEXT)
	value_texts = convert_column(first_values, text_conversion)
	value_names = cast(list[str], value_texts.tolist())

	return value_names


def write_decimal(decimal: float) -> str:
	"""
	Return a decimal written as a text, without decimal part when it is whole.

	.. versionadded:: 0.1.0

	Parameters
	----------
	decimal
		The decimal.

	Returns
	-------
	str
		The text.

	Examples
	--------
	>>> from numdaplot.tables.pivot.pivoted_frame import write_decimal
	>>> write_decimal(8.0)
	'8'
	>>> write_decimal(2.5)
	'2.5'
	"""
	if decimal.is_integer():
		whole_number = int(decimal)
		return str(whole_number)

	return str(decimal)


def number_row_groups(row_groups: list[NDArray[Any]], row_count: int) -> NDArray[Any]:
	"""
	Return the number of the group of each row.

	.. versionadded:: 0.1.0

	Parameters
	----------
	row_groups
		The rows of each group, every row being in one group.
	row_count
		The number of rows.

	Returns
	-------
	NDArray
		One group number per row.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.pivot.pivoted_frame import number_row_groups
	>>> number_row_groups([numpy.array([1]), numpy.array([0, 2])], 3)
	array([1, 0, 1])
	"""
	group_numbers = numpy.zeros(row_count, dtype=ROW_POSITION_DTYPE)

	for group_number, row_group in enumerate(row_groups):
		group_numbers[row_group] = group_number

	return group_numbers

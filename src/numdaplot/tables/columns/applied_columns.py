"""
Application of a function to columns of a Table.

.. versionadded:: 0.2.0
"""

from functools import partial
from typing import Any

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.arrays.creation.list_conversion import convert_list
from numdaplot.arrays.dates.time_function_values import apply_time_function
from numdaplot.arrays.mapping.mapped_values import find_mapping_result
from numdaplot.arrays.mapping.value_mapping import ValueMapping
from numdaplot.arrays.math_functions.math_function_values import apply_math_function
from numdaplot.dates.time_function import TimeFunction
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.math_functions.math_function import MathFunction
from numdaplot.tables.columns.replaced_columns import replace_frame_columns
from numdaplot.tables.columns.table_application import TableApplication
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import build_column_with_missing, find_column_missing, read_present_values
from numdaplot.tables.frames.time_zones import find_column_time_zone

APPLICATION_OPERATION = "Applying a function to {column_name!r}"


def apply_frame_columns(frame: pandas.DataFrame, application: TableApplication) -> pandas.DataFrame:
	"""
	Return the columns of a Table with a function applied to some of them, each at its place.

	.. versionadded:: 0.2.0

	Parameters
	----------
	frame
		The columns of a Table.
	application
		The function and the names of the columns it applies to.

	Returns
	-------
	pandas.DataFrame
		A new DataFrame, the other columns unchanged.

	Raises
	------
	ColumnNotFoundError
		When a column does not exist, before any column is changed.
	TimeZoneMismatchError
		When a column holds datetimes with a time zone.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.applied_columns import apply_frame_columns
	>>> frame = pandas.DataFrame({"area": [4.0, 9.0], "city": ["Pau", "Dax"]})
	>>> apply_frame_columns(frame, ndp.TableApplication(function=ndp.SquareRoot(), columns=["area"]))
	   area city
	0   2.0  Pau
	1   3.0  Dax
	"""
	function_application = partial(apply_to_column, function=application.function)
	applied_frame = replace_frame_columns(frame, application.columns, function_application)

	return applied_frame


def apply_to_column(column: Column, function: MathFunction | TimeFunction | ValueMapping) -> Column:
	"""
	Return a Table column with a function applied to each present value.

	.. versionadded:: 0.2.0

	Parameters
	----------
	column
		A Table column, numbered from 0.
	function
		A math function, a time function or a value mapping.

	Returns
	-------
	pandas.Series
		A new column numbered from 0, missing where the column is missing, and where a mapping gives None.

	Raises
	------
	TimeZoneMismatchError
		When the column holds datetimes with a time zone.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.applied_columns import apply_to_column
	>>> apply_to_column(pandas.Series([1, None, 9], dtype="Int64"), ndp.SquareRoot()).tolist()
	[1.0, nan, 3.0]
	"""
	require_column_without_time_zone(column)
	present_values = read_present_values(column)
	missing = find_column_missing(column)

	if isinstance(function, ValueMapping):
		mapped_column = map_present_values(present_values, missing, function)
		return mapped_column

	if isinstance(function, TimeFunction):
		time_values = apply_time_function(present_values, function)
		time_column = build_column_with_missing(time_values, missing)
		return time_column

	transformed_values = apply_math_function(present_values, function)
	transformed_column = build_column_with_missing(transformed_values, missing)

	return transformed_column


def map_present_values(present_values: NDArray[Any], missing: NDArray[numpy.bool_], mapping: ValueMapping) -> Column:
	"""
	Return a Table column holding the new values a mapping gives to the present values of a column.

	A Table column accepts missing values of any type, so integers and booleans keep their type when the mapping
	gives None.

	.. versionadded:: 0.2.0

	Parameters
	----------
	present_values
		The present values of the column, in order.
	missing
		True at each missing position of the column.
	mapping
		The new value of each listed value, and what happens to the others.

	Returns
	-------
	pandas.Series
		A column numbered from 0, missing where the column is missing and where the mapping gives None.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.applied_columns import map_present_values
	>>> mapping = ndp.ValueMapping(changes=[ndp.ValueChange(7, None)], others=ndp.Unmatched.KEEP)
	>>> map_present_values(numpy.array([1, 7]), numpy.array([False, True, False]), mapping).tolist()
	[1, <NA>, <NA>]
	"""
	mapping_result = find_mapping_result(present_values, mapping)
	new_values = mapping_result.new_values
	cleared_list = [new_value is None for new_value in new_values]
	cleared = numpy.array(cleared_list, dtype=numpy.bool_)
	present = ~missing
	mapped_missing = missing.copy()
	mapped_missing[present] = cleared
	kept_values = [new_value for new_value in new_values if new_value is not None]
	stored_values = convert_list(kept_values, mapping_result.result_type)
	mapped_column = build_column_with_missing(stored_values, mapped_missing)

	return mapped_column


def require_column_without_time_zone(column: Column) -> None:
	"""
	Check that a Table column holds no datetime with a time zone, which the functions read as UTC clock times.

	.. versionadded:: 0.2.0

	Parameters
	----------
	column
		A Table column.

	Raises
	------
	TimeZoneMismatchError
		When the column holds datetimes with a time zone.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.applied_columns import require_column_without_time_zone
	>>> times = pandas.Series(pandas.to_datetime(["2026-03-14 23:30"]), name="pickup").dt.tz_localize("UTC")
	>>> try:
	... 	require_column_without_time_zone(times)
	... except ndp.TimeZoneMismatchError as error:
	... 	print(error)
	Applying a function to 'pickup' needs datetimes without a time zone.
	"""
	time_zone = find_column_time_zone(column)
	if time_zone is None:
		return

	column_name = str(column.name)
	operation = APPLICATION_OPERATION.format(column_name=column_name)
	raise TimeZoneMismatchError(operation, False)

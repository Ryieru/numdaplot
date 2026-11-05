"""
Description of the columns of a Table.

.. versionadded:: 0.1.0
"""

from datetime import UTC, datetime
from typing import Any
from zoneinfo import ZoneInfo

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.arrays.conversion.python_values import to_python_list
from numdaplot.data_types.numpy_mapping import from_numpy_dtype, to_numpy_dtype
from numdaplot.data_types.type import Type
from numdaplot.data_types.value_family import ValueFamily, find_family
from numdaplot.dates.time_zone import TimeZone
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.statistics.statistic import Statistic
from numdaplot.tables.aggregation.result_column import build_result_column, compute_cell
from numdaplot.tables.aggregation.statistic_name import name_statistic
from numdaplot.tables.columns.column_names import require_known_columns
from numdaplot.tables.description.description import DEFAULT_FUNCTIONS, Description
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import build_column, find_column_type, read_present_values
from numdaplot.tables.frames.time_zones import attribute_source_time_zone, find_column_time_zone

STATISTIC_COLUMN_NAME = "statistic"
SINGLE_FAMILY_COUNT = 1


def describe_frame(frame: pandas.DataFrame, description: Description) -> pandas.DataFrame:
	"""
	Return statistics of columns of a Table, one row per statistic and one column per described column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	description
		The statistics and the columns to describe.

	Returns
	-------
	pandas.DataFrame
		A first ``statistic`` column naming each statistic, then one column per described column.
		A cell is missing when the statistic does not apply to the column or finds no value.

	Raises
	------
	ColumnNotFoundError
		When a described column does not exist.
	DuplicateColumnError
		When a described column is named ``statistic``.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.description.described_frame import describe_frame
	>>> frame = pandas.DataFrame({"price": [1.0, 3.0]})
	>>> describe_frame(frame, ndp.Description(functions=[ndp.Count(), ndp.Mean()]))
	        statistic  price
	0  count_excluded    2.0
	1            mean    2.0
	"""
	functions = list[Statistic](DEFAULT_FUNCTIONS)
	if description.functions is not None:
		functions = description.functions

	described_names = find_described_columns(frame, description)
	statistic_names = [name_statistic(function) for function in functions]
	text_dtype = to_numpy_dtype(Type.TEXT)
	statistic_values = numpy.array(statistic_names, dtype=text_dtype)
	statistic_column = build_column(statistic_values)
	described_columns = {STATISTIC_COLUMN_NAME: statistic_column}

	for column_name in described_names:
		column = frame[column_name]
		described_column = describe_column(column, functions)
		described_columns[column_name] = described_column

	function_count = len(functions)
	row_numbers = pandas.RangeIndex(function_count)
	described_frame = pandas.DataFrame(described_columns, index=row_numbers)

	return described_frame


def find_described_columns(frame: pandas.DataFrame, description: Description) -> list[str]:
	"""
	Return the names of the columns to describe.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.
	description
		The settings of the description.

	Returns
	-------
	list[str]
		The given names, or every number column in the order of the Table.

	Raises
	------
	ColumnNotFoundError
		When a given column does not exist.
	DuplicateColumnError
		When a described column is named ``statistic``.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.description.described_frame import find_described_columns
	>>> frame = pandas.DataFrame({"city": pandas.array(["Pau"], dtype="string"), "price": [1.5]})
	>>> find_described_columns(frame, ndp.Description())
	['price']
	"""
	column_names = [str(column_name) for column_name in frame.columns]
	described_names = list[str]()
	if description.columns is not None:
		require_known_columns(description.columns, column_names)
		described_names = description.columns
	else:
		described_names = find_number_columns(frame)

	if STATISTIC_COLUMN_NAME in described_names:
		raise DuplicateColumnError(STATISTIC_COLUMN_NAME)

	return described_names


def find_number_columns(frame: pandas.DataFrame) -> list[str]:
	"""
	Return the names of the columns holding numbers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.

	Returns
	-------
	list[str]
		The names of the integer and decimal columns, in order.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.description.described_frame import find_number_columns
	>>> find_number_columns(pandas.DataFrame({"price": [1.5], "paid": pandas.array([True], dtype="boolean")}))
	['price']
	"""
	number_names = list[str]()

	for column_name in frame.columns:
		column = frame[column_name]
		column_type = find_column_type(column)
		column_family = find_family(column_type)
		if column_family == ValueFamily.NUMBER:
			number_name = str(column_name)
			number_names.append(number_name)

	return number_names


def describe_column(column: Column, functions: list[Statistic]) -> Column:
	"""
	Return the statistics of one column, missing where a statistic does not apply or finds no value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column.
	functions
		The statistics, one result each.

	Returns
	-------
	Column
		One result per statistic. When the results mix kinds of values, such as a count and a text,
		every result is written as a text.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.description.described_frame import describe_column
	>>> describe_column(pandas.Series(["b", "a"], dtype="string"), [ndp.Count(), ndp.Min(), ndp.Mean()]).tolist()
	['2', 'a', <NA>]
	"""
	present_values = read_present_values(column)
	value_count = len(column)
	results = [compute_description_cell(present_values, function, value_count) for function in functions]
	present_results = [result for result in results if result is not None]
	result_families = {find_result_family(result) for result in present_results}
	family_count = len(result_families)
	time_zone = find_column_time_zone(column)
	if family_count > SINGLE_FAMILY_COUNT:
		results = [convert_result_to_text(result, time_zone) for result in results]

	utc_column = build_result_column(results)
	described_column = attribute_source_time_zone(utc_column, column)

	return described_column


def compute_description_cell(
	present_values: NDArray[Any],
	statistic: Statistic,
	value_count: int,
) -> NDArray[Any] | None:
	"""
	Return a statistic of present values, or nothing when it does not apply or finds no value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	present_values
		One-dimensional values without missing value.
	statistic
		Any statistic of numdaplot.
	value_count
		The number of values before the missing ones were left out.

	Returns
	-------
	NDArray or None
		The result as a one-value array, or ``None``.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.description.described_frame import compute_description_cell
	>>> texts = numpy.array(["b", "a"], dtype="T")
	>>> compute_description_cell(texts, ndp.Min(), 2)
	array(['a'], dtype=StringDType(na_object=nan))
	>>> print(compute_description_cell(texts, ndp.Mean(), 2))
	None
	"""
	try:
		result = compute_cell(present_values, statistic, value_count)
	except IncompatibleTypesError:
		return None

	return result


def find_result_family(result: NDArray[Any]) -> ValueFamily:
	"""
	Return the family of the type of a result.

	.. versionadded:: 0.1.0

	Parameters
	----------
	result
		A one-value array.

	Returns
	-------
	ValueFamily
		The family of its type.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.description.described_frame import find_result_family
	>>> find_result_family(numpy.array([2]))
	<ValueFamily.NUMBER: 1>
	"""
	result_type = from_numpy_dtype(result.dtype)
	result_family = find_family(result_type)

	return result_family


def convert_result_to_text(result: NDArray[Any] | None, time_zone: TimeZone | None) -> NDArray[Any] | None:
	"""
	Return a result written as a text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	result
		A one-value array, or ``None``.
	time_zone
		The time zone of the described column: a datetime result, computed as a UTC clock time, is written
		in this zone with its offset. ``None`` when the column has no zone.

	Returns
	-------
	NDArray or None
		A one-text array, or ``None`` when there is no result.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.description.described_frame import convert_result_to_text
	>>> convert_result_to_text(numpy.array([2]), None)
	array(['2'], dtype=StringDType(na_object=nan))
	"""
	if result is None:
		return None

	python_values = to_python_list(result)
	single_value = python_values[0]
	shown_value = single_value
	if time_zone is not None and isinstance(single_value, datetime):
		utc_datetime = single_value.replace(tzinfo=UTC)
		zone_info = ZoneInfo(time_zone.name)
		shown_value = utc_datetime.astimezone(zone_info)

	result_text = str(shown_value)
	text_dtype = to_numpy_dtype(Type.TEXT)
	text_result = numpy.array([result_text], dtype=text_dtype)

	return text_result

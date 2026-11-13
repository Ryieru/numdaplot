"""
Exact writing of the decimal columns of a Table in a JSON file.

pandas writes decimals with 10 digits after the point at most, which changes values such as ``1 / 3``.

.. versionadded:: 0.1.0
"""

import json
from typing import Any, cast

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.data_types.numpy_mapping import from_numpy_dtype
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.named_column_errors import NamedColumnErrors

DECIMAL_KIND = "f"
DOUBLE_DTYPE = numpy.dtype(numpy.float64)
JSON_FORMAT_NAME = "JSON"
JSON_NULL = "null"
NAN_TEXT = "nan"
DECIMAL_FORMAT = "%.{decimals}f"
CELL_SEPARATOR = ":"
CELL_JOINER = ","
OBJECT_START = "{"
OBJECT_END = "}"
LINE_END = "\n"
RECORDS_ORIENTATION = "records"
ISO_DATE_FORMAT = "iso"
FIRST_CHARACTER_AFTER_BRACE = 1
LAST_CHARACTER_BEFORE_BRACE = -1


def is_decimal_column(column: Column) -> bool:
	"""
	Return whether a column holds decimals, stored by pandas with or without missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column.

	Returns
	-------
	bool
		True for a column of 32 or 64 bit decimals.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.files.json_decimals import is_decimal_column
	>>> is_decimal_column(pandas.Series([1.5], dtype="Float64")), is_decimal_column(pandas.Series([1]))
	(True, False)
	"""
	is_decimal = column.dtype.kind == DECIMAL_KIND

	return is_decimal


def read_decimals(column: Column) -> NDArray[Any]:
	"""
	Return the decimals of a column, in their number of bits, NaN for a missing value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A decimal column.

	Returns
	-------
	NDArray
		The values.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.files.json_decimals import read_decimals
	>>> read_decimals(pandas.Series([1.5, None], dtype="Float32"))
	array([1.5, nan], dtype=float32)
	"""
	dtype_name = str(column.dtype)
	numpy_dtype = numpy.dtype(dtype_name.lower())
	values = column.to_numpy(dtype=numpy_dtype, na_value=numpy.nan)

	return values


def has_decimal_column(frame: pandas.DataFrame) -> bool:
	"""
	Return whether a frame holds a column of decimals.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table.

	Returns
	-------
	bool
		True when at least one column holds decimals.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.files.json_decimals import has_decimal_column
	>>> has_decimal_column(pandas.DataFrame({"count": [1], "price": [1.5]}))
	True
	"""
	column_names = list[str](frame.columns)

	for column_name in column_names:
		column = frame[column_name]
		is_decimal = is_decimal_column(column)
		if is_decimal:
			return True

	return False


def require_finite_values(values: NDArray[Any]) -> None:
	"""
	Check that decimals hold no infinite value, which JSON cannot write.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The decimals, NaN for a missing value.

	Raises
	------
	ValueConversionError
		At the first infinite value.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.json_decimals import require_finite_values
	>>> try:
	... 	require_finite_values(numpy.array([1.5, numpy.inf]))
	... except ndp.ValueConversionError as error:
	... 	print(error)
	Cannot store the FLOAT64 value inf as JSON without losing information.
	"""
	is_infinite = numpy.isinf(values)
	has_infinite = bool(is_infinite.any())
	if not has_infinite:
		return

	infinite_values = values[is_infinite]
	first_infinite = float(infinite_values[0])
	column_type = from_numpy_dtype(values.dtype)
	raise ValueConversionError(column_type.name, JSON_FORMAT_NAME, first_infinite)


def write_shortest_texts(values: NDArray[Any]) -> list[str]:
	"""
	Return decimals as the shortest texts giving the same values in their number of bits.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The finite decimals, NaN for a missing value.

	Returns
	-------
	list[str]
		One JSON number per value, ``null`` for a missing value.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.files.json_decimals import write_shortest_texts
	>>> write_shortest_texts(numpy.array([1 / 3, numpy.nan]))
	['0.3333333333333333', 'null']
	>>> write_shortest_texts(numpy.array([0.1], dtype="float32"))
	['0.1']
	"""
	if values.dtype == DOUBLE_DTYPE:
		python_values = cast(list[float], values.tolist())
		texts = list(map(repr, python_values))
	else:
		# A Python float would write a 32 bit decimal widened to 64 bits, with its rounding error.
		numpy_texts = values.astype(str)
		texts = cast(list[str], numpy_texts.tolist())

	missing_positions = numpy.flatnonzero(numpy.isnan(values))
	for position in missing_positions:
		missing_position = int(position)
		texts[missing_position] = JSON_NULL

	return texts


def write_rounded_texts(values: NDArray[Any], decimals: int) -> list[str]:
	"""
	Return decimals rounded to a number of decimals, keeping their zeros as in a CSV file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The finite decimals, NaN for a missing value.
	decimals
		The number of decimals.

	Returns
	-------
	list[str]
		One JSON number per value, ``null`` for a missing value.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.files.json_decimals import write_rounded_texts
	>>> write_rounded_texts(numpy.array([1.5, numpy.nan]), 2)
	['1.50', 'null']
	"""
	decimal_format = DECIMAL_FORMAT.format(decimals=decimals)
	python_values = cast(list[float], values.tolist())
	rounded_texts = [JSON_NULL if value != value else decimal_format % value for value in python_values]

	return rounded_texts


def write_decimal_cells(column: Column, column_name: str, decimals: int | None) -> list[str]:
	"""
	Return the name and the value of a decimal column, as they appear in each object of a JSON file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A decimal column.
	column_name
		The name of the column.
	decimals
		The number of decimals written, every digit of each value when ``None``.

	Returns
	-------
	list[str]
		One text per row.

	Raises
	------
	ValueConversionError
		At the first infinite value.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.files.json_decimals import write_decimal_cells
	>>> write_decimal_cells(pandas.Series([0.1 + 0.2]), "price", None)
	['"price":0.30000000000000004']
	"""
	values = read_decimals(column)
	with NamedColumnErrors(column):
		require_finite_values(values)

	if decimals is None:
		value_texts = write_shortest_texts(values)
	else:
		value_texts = write_rounded_texts(values, decimals)

	name_text = json.dumps(column_name, ensure_ascii=False)
	cell_start = name_text + CELL_SEPARATOR
	cells = [cell_start + value_text for value_text in value_texts]

	return cells


def write_other_cells(frame: pandas.DataFrame) -> list[str]:
	"""
	Return the names and the values of columns without decimals, as they appear in each object of a JSON file.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		Columns without decimals.

	Returns
	-------
	list[str]
		One text per row, written by pandas: ``null``, ISO 8601 dates and durations.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.files.json_decimals import write_other_cells
	>>> write_other_cells(pandas.DataFrame({"city": ["Paris", None], "count": [1, 2]}))
	['"city":"Paris","count":1', '"city":null,"count":2']
	"""
	# Some versions of the pandas stubs leave the parameter types of to_json unknown.
	json_frame = cast(Any, frame)
	lines_text = cast(
		str,
		json_frame.to_json(orient=RECORDS_ORIENTATION, lines=True, force_ascii=False, date_format=ISO_DATE_FORMAT),
	)
	stripped_text = lines_text.removesuffix(LINE_END)
	# JSON writes a line break inside a text as an escape, so each line is one object.
	lines = stripped_text.split(LINE_END)
	cells = [line[FIRST_CHARACTER_AFTER_BRACE:LAST_CHARACTER_BEFORE_BRACE] for line in lines]

	return cells


def write_exact_objects(frame: pandas.DataFrame, decimals: int | None) -> list[str]:
	"""
	Return one JSON object per row, the columns staying in their order.

	Neighbor columns without decimals are written together by pandas, which is much faster than one by one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table, at least one holding decimals.
	decimals
		The number of decimals written, every digit of each value when ``None``.

	Returns
	-------
	list[str]
		One object per row.

	Raises
	------
	ValueConversionError
		At the first infinite value.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.files.json_decimals import write_exact_objects
	>>> write_exact_objects(pandas.DataFrame({"city": ["Paris"], "price": [1 / 3]}), None)
	['{"city":"Paris","price":0.3333333333333333}']
	"""
	if frame.empty:
		return []

	cell_groups = list[list[str]]()
	other_names = list[str]()

	for column_name in list[str](frame.columns):
		column = frame[column_name]
		is_decimal = is_decimal_column(column)
		if not is_decimal:
			other_names.append(column_name)
			continue

		if other_names != []:
			other_cells = write_other_cells(frame[other_names])
			cell_groups.append(other_cells)
			other_names = list[str]()

		decimal_cells = write_decimal_cells(column, column_name, decimals)
		cell_groups.append(decimal_cells)

	if other_names != []:
		last_cells = write_other_cells(frame[other_names])
		cell_groups.append(last_cells)

	row_cells = zip(*cell_groups, strict=True)
	rows = map(CELL_JOINER.join, row_cells)
	objects = [OBJECT_START + row + OBJECT_END for row in rows]

	return objects

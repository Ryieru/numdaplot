"""
Conversion of Table columns to number types.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.column_storage.column import Column
from numdaplot.column_storage.column_values import (
	build_column_with_missing,
	find_column_missing,
	find_column_type,
	read_present_values,
)
from numdaplot.column_storage.pandas_decimals import restore_exact_decimals
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.types.numpy_mapping import to_numpy_dtype
from numdaplot.types.type import Type

DECIMAL_KIND = "f"
FAILED_PARSE = "coerce"
PYTHON_OBJECT_DTYPE = numpy.dtype(object)
IGNORED_FLOAT_ERROR = "ignore"


def convert_numbers(column: Column, target_type: Type) -> Column:
	"""
	Return a number column converted to another number type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A number column.
	target_type
		The new number type.

	Returns
	-------
	Column
		The converted column. Decimals may be rounded to the precision of a smaller decimal type.

	Raises
	------
	ValueConversionError
		When a value does not fit: a decimal with a fractional part converted to an integer,
		or a number out of the range of the new type.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.number_conversion import convert_numbers
	>>> convert_numbers(pandas.Series([2.0, None]), ndp.Type.INT64).tolist()
	[2, <NA>]
	"""
	source_type = find_column_type(column)
	missing = find_column_missing(column)
	present_values = read_present_values(column)
	converted_values = store_numbers(present_values, target_type)
	require_no_lost_value(present_values, converted_values, source_type, target_type)
	converted_column = build_column_with_missing(converted_values, missing)

	return converted_column


def parse_numbers(column: Column, target_type: Type) -> Column:
	"""
	Return a text or category column read as numbers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A text or category column.
	target_type
		The number type to read the texts as.

	Returns
	-------
	Column
		The numbers, missing values staying missing.

	Raises
	------
	ValueConversionError
		At the first text that is not a number, or whose number does not fit the type.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.number_conversion import parse_numbers
	>>> parse_numbers(pandas.Series(["2.5", "1e3"], dtype="string"), ndp.Type.FLOAT64).tolist()
	[2.5, 1000.0]
	"""
	source_type = find_column_type(column)
	missing = find_column_missing(column)
	texts = read_present_values(column)
	object_texts = texts.astype(PYTHON_OBJECT_DTYPE)
	parsed_values = pandas.to_numeric(object_texts, errors=FAILED_PARSE)
	read_numbers = numpy.asarray(parsed_values)
	failed = numpy.zeros(texts.shape, dtype=numpy.bool_)
	if read_numbers.dtype.kind == DECIMAL_KIND:
		failed = numpy.isnan(read_numbers)

	require_no_failed_value(texts, failed, source_type, target_type)
	numbers = restore_exact_decimals(object_texts, read_numbers)
	converted_values = store_numbers(numbers, target_type)
	lost = find_lost_values(numbers, converted_values)
	require_no_failed_value(texts, lost, source_type, target_type)
	parsed_column = build_column_with_missing(converted_values, missing)

	return parsed_column


def store_numbers(values: NDArray[Any], target_type: Type) -> NDArray[Any]:
	"""
	Return numbers stored in a number type, even when some do not fit.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Numbers in a numpy dtype.
	target_type
		The number type to store them as.

	Returns
	-------
	NDArray
		The stored numbers; check them with ``find_lost_values``.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.number_conversion import store_numbers
	>>> store_numbers(numpy.array([2.0]), ndp.Type.INT8)
	array([2], dtype=int8)
	"""
	target_dtype = to_numpy_dtype(target_type)
	with numpy.errstate(invalid=IGNORED_FLOAT_ERROR, over=IGNORED_FLOAT_ERROR):
		stored_values = values.astype(target_dtype)

	return stored_values


def find_lost_values(values: NDArray[Any], stored_values: NDArray[Any]) -> NDArray[numpy.bool_]:
	"""
	Return which numbers changed when stored in another number type, beyond the rounding of decimals.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The original numbers.
	stored_values
		The same numbers stored in another type.

	Returns
	-------
	NDArray[numpy.bool_]
		For a decimal type, True where a finite number became infinite. For an integer type,
		True where the stored number differs from the original one.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.conversions.number_conversion import find_lost_values
	>>> find_lost_values(numpy.array([2.0, 2.5]), numpy.array([2, 2]))
	array([False,  True])
	"""
	if stored_values.dtype.kind == DECIMAL_KIND:
		finite = numpy.isfinite(values)
		infinite = numpy.isinf(stored_values)
		overflowed = finite & infinite
		return overflowed

	with numpy.errstate(invalid=IGNORED_FLOAT_ERROR, over=IGNORED_FLOAT_ERROR):
		restored_values = stored_values.astype(values.dtype)

	changed = restored_values != values

	return changed


def require_no_lost_value(
	values: NDArray[Any], stored_values: NDArray[Any], source_type: Type, target_type: Type
) -> None:
	"""
	Check that numbers kept their value when stored in another number type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The original numbers.
	stored_values
		The same numbers stored in the new type.
	source_type
		The type of the original numbers.
	target_type
		The new type.

	Raises
	------
	ValueConversionError
		At the first number that changed.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.number_conversion import require_no_lost_value
	>>> try:
	... 	require_no_lost_value(numpy.array([2.0, 2.5]), numpy.array([2, 2]), ndp.Type.FLOAT64, ndp.Type.INT64)
	... except ndp.ValueConversionError as error:
	... 	print(error)
	Cannot store the FLOAT64 value 2.5 as INT64 without losing information.
	"""
	lost = find_lost_values(values, stored_values)
	require_no_failed_value(values, lost, source_type, target_type)


def require_no_failed_value(
	values: NDArray[Any], failed: NDArray[numpy.bool_], source_type: Type, target_type: Type
) -> None:
	"""
	Check that no value failed its conversion.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The original values, texts or numbers.
	failed
		True at each value that failed.
	source_type
		The type of the original values.
	target_type
		The new type.

	Raises
	------
	ValueConversionError
		At the first failed value, which the message shows.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.number_conversion import require_no_failed_value
	>>> texts = numpy.array(["12", "abc"])
	>>> failed = numpy.array([False, True])
	>>> try:
	... 	require_no_failed_value(texts, failed, ndp.Type.TEXT, ndp.Type.INT64)
	... except ndp.ValueConversionError as error:
	... 	print(error)
	Cannot store the TEXT value 'abc' as INT64 without losing information.
	"""
	has_failure = bool(failed.any())
	if not has_failure:
		return

	failed_values = values[failed]
	raw_values = failed_values.tolist()
	python_values = cast(list[Any], raw_values)
	rejected_value = python_values[0]
	raise ValueConversionError(source_type.name, target_type.name, rejected_value)

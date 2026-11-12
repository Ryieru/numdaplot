"""
Conversion of the values of an Array to another type.

.. versionadded:: 0.2.0
"""

from typing import Any

from numpy.typing import NDArray

from numdaplot.conversions.array_conversion import ArrayConversion
from numdaplot.conversions.converted_column import convert_column
from numdaplot.data_types.number_types import INTEGER_TYPES
from numdaplot.data_types.type import Type
from numdaplot.errors.unsupported_missing_error import UnsupportedMissingError
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import (
	build_column,
	find_column_missing,
	find_column_type,
	read_array_values,
)

INTEGER_ADVICE = "Convert to FLOAT64 instead, which can be missing."
BOOLEAN_ADVICE = (
	"Keep the present values first with select(ndp.IsPresent()), which gives one dimension, or convert the column of "
	"the Table, which can hold missing booleans."
)


def convert_array_values(values: NDArray[Any], conversion: ArrayConversion) -> NDArray[Any]:
	"""
	Return the values of an Array converted to another type, in the same shape, missing values staying missing.

	The values go through a Table column, so that an Array accepts the conversions of a Table column.

	.. versionadded:: 0.2.0

	Parameters
	----------
	values
		The values of an Array.
	conversion
		The new type, and the date format or the rule reading numbers as booleans.

	Returns
	-------
	NDArray
		The converted values, in the numpy form an Array stores.

	Raises
	------
	IncompatibleTypesError
		When the conversion is not accepted, such as a boolean to a date.
	InvalidConversionError
		When the format or the boolean rule does not apply to the conversion.
	ValueConversionError
		When a value cannot be stored in the new type without losing information.
	TimeOverflowError
		When a date read or converted is outside what the new type can hold.
	UnsupportedMissingError
		When integers or booleans would hold a missing value, which an Array cannot hold.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.converted_array import convert_array_values
	>>> convert_array_values(numpy.array([[1, 2], [3, 4]]), ndp.ArrayConversion(dtype=ndp.Type.FLOAT64))
	array([[1., 2.],
	       [3., 4.]])
	"""
	flat_values = values.ravel()
	column = build_column(flat_values)
	converted_column = convert_column(column, conversion)
	require_missing_storable(converted_column)
	converted_values = read_array_values(converted_column)
	shaped_values = converted_values.reshape(values.shape)

	return shaped_values


def require_missing_storable(column: Column) -> None:
	"""
	Check that a converted column holds no missing value in a type an Array cannot hold missing.

	.. versionadded:: 0.2.0

	Parameters
	----------
	column
		The converted values, as a Table column.

	Raises
	------
	UnsupportedMissingError
		When integers or booleans hold a missing value, with advice fitting an Array.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.converted_array import require_missing_storable
	>>> try:
	... 	require_missing_storable(pandas.Series([1, None], dtype="Int64"))
	... except ndp.UnsupportedMissingError as error:
	... 	print(error)
	INT64 values cannot be missing in an Array. Convert to FLOAT64 instead, which can be missing.
	"""
	missing = find_column_missing(column)
	any_missing = missing.any()
	has_missing = bool(any_missing)
	if not has_missing:
		return

	column_type = find_column_type(column)
	if column_type in INTEGER_TYPES:
		raise UnsupportedMissingError(column_type.name, advice=INTEGER_ADVICE)

	if column_type == Type.BOOL:
		raise UnsupportedMissingError(column_type.name, advice=BOOLEAN_ADVICE)

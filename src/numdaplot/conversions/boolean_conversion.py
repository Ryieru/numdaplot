"""
Conversion of Table columns between booleans and numbers.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy

from numdaplot.conversions.boolean_rule import BooleanRule
from numdaplot.data_types.type import Type
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import (
	build_column_with_missing,
	find_column_missing,
	find_column_type,
	read_present_values,
)
from numdaplot.tables.frames.frame_normalization import convert_to_type

FALSE_NUMBER = 0
TRUE_NUMBER = 1


def convert_booleans_to_numbers(column: Column, target_type: Type) -> Column:
	"""
	Return a boolean column as numbers: 1 for ``True`` and 0 for ``False``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A ``BOOL`` column.
	target_type
		A number type.

	Returns
	-------
	Column
		The column of numbers, missing values staying missing.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.boolean_conversion import convert_booleans_to_numbers
	>>> flags = pandas.Series([True, None, False], dtype="boolean")
	>>> convert_booleans_to_numbers(flags, ndp.Type.FLOAT64).tolist()
	[1.0, nan, 0.0]
	"""
	number_column = convert_to_type(column, target_type)

	return number_column


def convert_numbers_to_booleans(column: Column, rule: BooleanRule) -> Column:
	"""
	Return a number column as booleans, each number read by a rule.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A number column.
	rule
		``ZERO_ONE`` to accept only 0 and 1, ``NONZERO_TRUE`` to read every number but 0 as ``True``.

	Returns
	-------
	Column
		A ``BOOL`` column, missing values staying missing.

	Raises
	------
	ValueConversionError
		With ``ZERO_ONE``, at the first number that is neither 0 nor 1.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.boolean_conversion import convert_numbers_to_booleans
	>>> numbers = pandas.Series([1, None, 0], dtype="Int64")
	>>> convert_numbers_to_booleans(numbers, ndp.BooleanRule.ZERO_ONE).tolist()
	[True, <NA>, False]
	"""
	missing = find_column_missing(column)
	numbers = read_present_values(column)
	if rule == BooleanRule.ZERO_ONE:
		source_type = find_column_type(column)
		require_zero_or_one(numbers, source_type)

	is_true = numbers != FALSE_NUMBER
	boolean_column = build_column_with_missing(is_true, missing)

	return boolean_column


def require_zero_or_one(numbers: numpy.typing.NDArray[numpy.number], source_type: Type) -> None:
	"""
	Check that every number is 0 or 1.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numbers
		The present numbers of a column.
	source_type
		The type of the column, named in the error.

	Raises
	------
	ValueConversionError
		At the first number that is neither 0 nor 1.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.conversions.boolean_conversion import require_zero_or_one
	>>> try:
	... 	require_zero_or_one(numpy.array([1, 2, 0]), ndp.Type.INT64)
	... except ndp.ValueConversionError as error:
	... 	print(error)
	Cannot store the INT64 value 2 as BOOL without losing information.
	"""
	is_false = numbers == FALSE_NUMBER
	is_true = numbers == TRUE_NUMBER
	is_boolean = is_false | is_true
	is_other = ~is_boolean
	has_other = bool(is_other.any())
	if not has_other:
		return

	other_numbers = numbers[is_other]
	raw_numbers = other_numbers.tolist()
	python_numbers = cast(list[Any], raw_numbers)
	first_other_number = python_numbers[0]
	raise ValueConversionError(source_type.name, Type.BOOL.name, first_other_number)

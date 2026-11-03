"""
Conversion of a Table column to another type.

.. versionadded:: 0.1.0
"""

from numdaplot.data_types.type import Type
from numdaplot.data_types.value_family import ValueFamily, find_family
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.tables.columns.number_conversion import convert_numbers, parse_numbers
from numdaplot.tables.columns.text_conversion import parse_booleans
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import find_column_type
from numdaplot.tables.frames.frame_normalization import convert_to_type

CONVERT_OPERATION = "convert"
WRITABLE_FAMILIES = frozenset({ValueFamily.NUMBER, ValueFamily.BOOL, ValueFamily.TEXT})


def convert_column(column: Column, target_type: Type) -> Column:
	"""
	Return a Table column converted to another type, missing values staying missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column.
	target_type
		The new type.

	Returns
	-------
	Column
		The converted column, or a copy when it already has the type. Numbers, booleans and categories
		become texts as Python writes them, such as ``2.5`` or ``True``.

	Raises
	------
	IncompatibleTypesError
		When the conversion is not accepted, such as a boolean to a number, or any date conversion.
	ValueConversionError
		When a value cannot be stored in the new type without losing information.

	Examples
	--------
	>>> import pandas
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.converted_column import convert_column
	>>> convert_column(pandas.Series(["1", None, "3"], dtype="string"), ndp.Type.INT64).tolist()
	[1, <NA>, 3]
	"""
	source_type = find_column_type(column)
	source_family = find_family(source_type)
	target_family = find_family(target_type)
	if source_type == target_type:
		column_copy = column.copy()
		return column_copy

	if target_type == Type.CATEGORY and source_family in WRITABLE_FAMILIES:
		text_column = convert_to_type(column, Type.TEXT)
		category_column = convert_to_type(text_column, Type.CATEGORY)
		return category_column

	if target_type == Type.TEXT and source_family in WRITABLE_FAMILIES:
		text_column = convert_to_type(column, Type.TEXT)
		return text_column

	if source_family == ValueFamily.NUMBER and target_family == ValueFamily.NUMBER:
		number_column = convert_numbers(column, target_type)
		return number_column

	if source_family == ValueFamily.TEXT and target_family == ValueFamily.NUMBER:
		parsed_column = parse_numbers(column, target_type)
		return parsed_column

	if source_family == ValueFamily.TEXT and target_type == Type.BOOL:
		boolean_column = parse_booleans(column)
		return boolean_column

	type_names = [source_type.name, target_type.name]
	raise IncompatibleTypesError(CONVERT_OPERATION, type_names)

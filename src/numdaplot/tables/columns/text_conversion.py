"""
Conversion of text columns to booleans.

.. versionadded:: 0.1.0
"""

import numpy

from numdaplot.data_types.type import Type
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.column_values import (
	build_column_with_missing,
	find_column_missing,
	find_column_type,
	read_present_values,
)

TRUE_TEXT = "true"
FALSE_TEXT = "false"


def parse_booleans(column: Column) -> Column:
	"""
	Return a text or category column read as booleans.

	``true`` and ``false`` are accepted whatever their case and the spaces around them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A text or category column.

	Returns
	-------
	Column
		A ``BOOL`` column, missing values staying missing.

	Raises
	------
	ValueConversionError
		At the first text that is neither ``true`` nor ``false``.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.columns.text_conversion import parse_booleans
	>>> parse_booleans(pandas.Series(["True", " false ", None], dtype="string")).tolist()
	[True, False, <NA>]
	"""
	source_type = find_column_type(column)
	missing = find_column_missing(column)
	texts = read_present_values(column)
	stripped_texts = numpy.strings.strip(texts)
	lowered_texts = numpy.strings.lower(stripped_texts)
	is_true = lowered_texts == TRUE_TEXT
	is_false = lowered_texts == FALSE_TEXT
	is_known = is_true | is_false
	is_unknown = ~is_known
	has_unknown = bool(is_unknown.any())
	if has_unknown:
		unknown_texts = texts[is_unknown]
		first_unknown_text = unknown_texts[0]
		raise ValueConversionError(source_type.name, Type.BOOL.name, first_unknown_text)

	boolean_column = build_column_with_missing(is_true, missing)

	return boolean_column

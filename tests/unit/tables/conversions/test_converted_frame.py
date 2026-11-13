"""
Unit tests of the conversion of columns of a Table to another type.

.. versionadded:: 0.2.0
"""

import pandas
import pytest

from numdaplot.column_storage.column_values import find_column_type
from numdaplot.conversions.table_conversion import TableConversion
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.conversions.converted_frame import convert_frame_columns
from numdaplot.types.type import Type

LOW_NAME = "low"
HIGH_NAME = "high"
LABEL_NAME = "label"
TEXT_DTYPE = "string"
LABELS = pandas.Series(["a", "b"], dtype=TEXT_DTYPE)
FRAME = pandas.DataFrame({LOW_NAME: [1.0, 2.0], HIGH_NAME: [3.0, 4.0], LABEL_NAME: LABELS})
SMALL_INTEGERS = TableConversion(columns=[LOW_NAME, HIGH_NAME], dtype=Type.INT8)
EXPECTED_COLUMN_NAMES = [LOW_NAME, HIGH_NAME, LABEL_NAME]
EXPECTED_HIGH_VALUES = [3, 4]
DECIMAL_FRAME = pandas.DataFrame({LOW_NAME: [1.0, 2.0], HIGH_NAME: [3.5, 4.0]})


def test_convert_frame_columns_converts_every_listed_column() -> None:
	"""
	Check that each listed column takes the new type at its place, the other columns unchanged.

	.. versionadded:: 0.2.0
	"""
	converted_frame = convert_frame_columns(FRAME, SMALL_INTEGERS)

	column_names = converted_frame.columns.tolist()
	low_type = find_column_type(converted_frame[LOW_NAME])
	high_type = find_column_type(converted_frame[HIGH_NAME])
	label_type = find_column_type(converted_frame[LABEL_NAME])
	high_values = converted_frame[HIGH_NAME].tolist()
	assert column_names == EXPECTED_COLUMN_NAMES
	assert low_type == Type.INT8
	assert high_type == Type.INT8
	assert label_type == Type.TEXT
	assert high_values == EXPECTED_HIGH_VALUES


def test_convert_frame_columns_names_the_failing_column() -> None:
	"""
	Check that a value that does not fit the new type raises ValueConversionError naming its column.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(ValueConversionError) as error_info:
		convert_frame_columns(DECIMAL_FRAME, SMALL_INTEGERS)

	assert error_info.value.column_name == HIGH_NAME

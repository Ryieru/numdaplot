"""
Unit tests of the conversion of the values of an Array to another type.

.. versionadded:: 0.2.0
"""

import numpy
import pandas
import pytest

from numdaplot.conversions import converted_array
from numdaplot.conversions.array_conversion import ArrayConversion
from numdaplot.conversions.converted_array import convert_array_values, require_missing_storable
from numdaplot.conversions.converted_column import convert_column
from numdaplot.conversions.table_conversion import TableConversion
from numdaplot.data_types.type import Type
from numdaplot.errors.unsupported_missing_error import UnsupportedMissingError
from numdaplot.tables.frames.column import Column

CONVERT_COLUMN_NAME = "convert_column"
GRID = numpy.array([[1, 2], [3, 4]])
EXPECTED_DECIMAL_GRID = [[1.0, 2.0], [3.0, 4.0]]
DECIMAL_CONVERSION = ArrayConversion(dtype=Type.FLOAT64)
INTEGERS_WITH_MISSING = pandas.Series([1, None], dtype="Int64")
BOOLEANS_WITH_MISSING = pandas.Series([True, None], dtype="boolean")
DECIMALS_WITH_MISSING = pandas.Series([1.5, None], dtype="float64")
INTEGERS_WITHOUT_MISSING = pandas.Series([1, 2], dtype="Int64")
INTEGER_MESSAGE = "INT64 values cannot be missing in an Array. Convert to FLOAT64 instead, which can be missing."
BOOLEAN_MESSAGE = (
	"BOOL values cannot be missing in an Array. Keep the present values first with select(ndp.IsPresent()), which "
	"gives one dimension, or convert the column of the Table, which can hold missing booleans."
)


class ColumnConversionRecorder:
	"""
	Column conversion recording the length of each column, then converting it as numdaplot does.

	.. versionadded:: 0.2.0
	"""

	def __init__(self) -> None:
		"""
		Start without recorded column.

		.. versionadded:: 0.2.0
		"""
		self.column_lengths = list[int]()

	def convert(self, column: Column, conversion: ArrayConversion | TableConversion) -> Column:
		"""
		Record the length of the column and convert it.

		.. versionadded:: 0.2.0

		Parameters
		----------
		column
			The values of the Array, as a Table column.
		conversion
			The new type.

		Returns
		-------
		Column
			The converted column.
		"""
		column_length = len(column)
		self.column_lengths.append(column_length)
		converted = convert_column(column, conversion)

		return converted


def test_convert_array_values_converts_a_flat_column_and_keeps_the_shape(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the values of a grid are converted as one column of 4 values, then given back their 2 by 2 shape.

	.. versionadded:: 0.2.0

	Parameters
	----------
	monkeypatch
		Records the columns given to the column conversion.
	"""
	recorder = ColumnConversionRecorder()
	monkeypatch.setattr(converted_array, CONVERT_COLUMN_NAME, recorder.convert)

	converted_values = convert_array_values(GRID, DECIMAL_CONVERSION)

	converted_grid = converted_values.tolist()
	assert recorder.column_lengths == [GRID.size]
	assert converted_grid == EXPECTED_DECIMAL_GRID


@pytest.mark.parametrize(
	("column", "expected_message"),
	[(INTEGERS_WITH_MISSING, INTEGER_MESSAGE), (BOOLEANS_WITH_MISSING, BOOLEAN_MESSAGE)],
)
def test_require_missing_storable_refuses_missing_integers_and_booleans(column: Column, expected_message: str) -> None:
	"""
	Check that integers and booleans with a missing value raise UnsupportedMissingError with their advice.

	.. versionadded:: 0.2.0

	Parameters
	----------
	column
		Converted values with a missing value.
	expected_message
		The message of the error.
	"""
	with pytest.raises(UnsupportedMissingError) as error_info:
		require_missing_storable(column)

	error_text = str(error_info.value)
	assert error_text == expected_message


@pytest.mark.parametrize("column", [DECIMALS_WITH_MISSING, INTEGERS_WITHOUT_MISSING])
def test_require_missing_storable_accepts_values_an_array_can_hold(column: Column) -> None:
	"""
	Check that decimals with a missing value, and integers without, are accepted.

	.. versionadded:: 0.2.0

	Parameters
	----------
	column
		Converted values an Array can hold.
	"""
	require_missing_storable(column)

"""
Unit tests of build_filled_values.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.arrays.creation.filled_values import build_filled_values
from numdaplot.errors.types.value_conversion_error import ValueConversionError
from numdaplot.positions.shape import Shape
from numdaplot.types.type import Type

GRID_SHAPE = Shape([2, 3])
ZERO = 0
DECIMAL_VALUE = 1.5
EXPECTED_ZEROS = [[0, 0, 0], [0, 0, 0]]
EXPECTED_DECIMAL_ZEROS = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
DECIMAL_KIND = "f"


def test_build_filled_values_repeats_the_value_in_the_shape() -> None:
	"""
	Check that every position holds the value.

	.. versionadded:: 0.1.0
	"""
	values = build_filled_values(GRID_SHAPE, ZERO, None)

	value_rows = values.tolist()
	assert value_rows == EXPECTED_ZEROS


def test_build_filled_values_stores_the_value_in_the_given_type() -> None:
	"""
	Check that an integer can be repeated as decimals.

	.. versionadded:: 0.1.0
	"""
	values = build_filled_values(GRID_SHAPE, ZERO, Type.FLOAT64)

	value_rows = values.tolist()
	assert value_rows == EXPECTED_DECIMAL_ZEROS
	assert values.dtype.kind == DECIMAL_KIND


def test_build_filled_values_rejects_a_decimal_stored_as_integer() -> None:
	"""
	Check that a decimal cannot fill an INT64 array.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError):
		build_filled_values(GRID_SHAPE, DECIMAL_VALUE, Type.INT64)

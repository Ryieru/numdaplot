"""
Unit tests of combine_values and check_shapes.

.. versionadded:: 0.1.0
"""

import re

import numpy
import pytest

from numdaplot.arrays.operations.combination import check_shapes, combine_values
from numdaplot.errors.positions.shape_mismatch_error import ShapeMismatchError
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.warnings.broadcast_warning import BroadcastWarning

ADDITION_SYMBOL = "+"
SUBTRACTION_SYMBOL = "-"
VALUES = [1, 2]
OTHER_VALUES = [10, 20]
GRID_VALUES = [[1, 2], [3, 4]]
THREE_VALUES = [1, 2, 3]
SCALAR = 10
TEXT_VALUE = "euros"
EXPECTED_SUM = [11, 22]
EXPECTED_REFLECTED_DIFFERENCE = [9, 8]
EXPECTED_MESSAGE = re.escape("Cannot apply + to INT64 and TEXT.")


def test_combine_values_combines_two_arrays_value_by_value() -> None:
	"""
	Check that two arrays of the same shape are added position by position.

	.. versionadded:: 0.1.0
	"""
	left = numpy.array(VALUES)
	right = numpy.array(OTHER_VALUES)

	combined_values = combine_values(left, right, numpy.add, ADDITION_SYMBOL)

	combined_list = combined_values.tolist()
	assert combined_list == EXPECTED_SUM


def test_combine_values_accepts_a_single_value_on_the_left() -> None:
	"""
	Check that a single value can be the left operand.

	.. versionadded:: 0.1.0
	"""
	right = numpy.array(VALUES)

	combined_values = combine_values(SCALAR, right, numpy.subtract, SUBTRACTION_SYMBOL)

	combined_list = combined_values.tolist()
	assert combined_list == EXPECTED_REFLECTED_DIFFERENCE


def test_combine_values_rejects_incompatible_types() -> None:
	"""
	Check that adding a text to integers raises IncompatibleTypesError naming both types.

	.. versionadded:: 0.1.0
	"""
	left = numpy.array(VALUES)

	with pytest.raises(IncompatibleTypesError, match=EXPECTED_MESSAGE):
		combine_values(left, TEXT_VALUE, numpy.add, ADDITION_SYMBOL)


def test_check_shapes_warns_when_an_array_is_stretched() -> None:
	"""
	Check that a row added to a grid emits a BroadcastWarning.

	.. versionadded:: 0.1.0
	"""
	grid = numpy.array(GRID_VALUES)
	row = numpy.array(VALUES)

	with pytest.warns(BroadcastWarning):
		check_shapes(grid, row)


def test_check_shapes_rejects_shapes_that_cannot_match() -> None:
	"""
	Check that three values cannot be combined with two.

	.. versionadded:: 0.1.0
	"""
	left = numpy.array(THREE_VALUES)
	right = numpy.array(VALUES)

	with pytest.raises(ShapeMismatchError):
		check_shapes(left, right)


@pytest.mark.filterwarnings("error")
def test_check_shapes_accepts_a_single_value_without_warning() -> None:
	"""
	Check that a single value never emits a warning.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(VALUES)

	check_shapes(values, SCALAR)

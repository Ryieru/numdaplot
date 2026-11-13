"""
Unit tests of ArrayLogic.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from typing import Any, cast

import numpy
import pytest

from numdaplot.arrays.array_data import read_stored_values
from numdaplot.arrays.array_logic import ArrayLogic
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError

LEFT_BOOLEANS = [True, True, False]
RIGHT_BOOLEANS = [True, False, False]
EXPECTED_AND = [True, False, False]
EXPECTED_OR = [True, True, False]
EXPECTED_NOT = [False, False, True]
EXPECTED_AND_WITH_TRUE = [True, True, False]
INTEGERS = [1, 0, 1]


def read_values(array: ArrayLogic) -> list[bool]:
	"""
	Return the values of an Array as a Python list.

	.. versionadded:: 0.1.0

	Parameters
	----------
	array
		The Array.

	Returns
	-------
	list[bool]
		Its values.
	"""
	numpy_values = read_stored_values(array)
	raw_values = numpy_values.tolist()
	value_list = cast(list[Any], raw_values)

	return value_list


def test_array_logic_combines_with_and() -> None:
	"""
	Check that & is True where both are True.

	.. versionadded:: 0.1.0
	"""
	left_values = numpy.array(LEFT_BOOLEANS)
	right_values = numpy.array(RIGHT_BOOLEANS)
	left = ArrayLogic._create(left_values)
	right = ArrayLogic._create(right_values)

	combined = left & right

	combined_list = read_values(combined)
	assert combined_list == EXPECTED_AND


def test_array_logic_combines_with_or() -> None:
	"""
	Check that | is True where at least one is True.

	.. versionadded:: 0.1.0
	"""
	left_values = numpy.array(LEFT_BOOLEANS)
	right_values = numpy.array(RIGHT_BOOLEANS)
	left = ArrayLogic._create(left_values)
	right = ArrayLogic._create(right_values)

	combined = left | right

	combined_list = read_values(combined)
	assert combined_list == EXPECTED_OR


def test_array_logic_combines_with_a_boolean_on_the_left() -> None:
	"""
	Check that a boolean can be on the left of &.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(LEFT_BOOLEANS)
	array = ArrayLogic._create(values)

	combined = True & array

	combined_list = read_values(combined)
	assert combined_list == EXPECTED_AND_WITH_TRUE


def test_array_logic_inverts_with_not() -> None:
	"""
	Check that ~ swaps True and False.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(LEFT_BOOLEANS)
	array = ArrayLogic._create(values)

	inverted = ~array

	inverted_list = read_values(inverted)
	assert inverted_list == EXPECTED_NOT


def test_array_logic_rejects_integers() -> None:
	"""
	Check that & refuses integers instead of combining their bits.

	.. versionadded:: 0.1.0
	"""
	integer_values = numpy.array(INTEGERS)
	boolean_values = numpy.array(LEFT_BOOLEANS)
	integers = ArrayLogic._create(integer_values)
	booleans = ArrayLogic._create(boolean_values)

	with pytest.raises(IncompatibleTypesError):
		_ = integers & booleans


def test_array_logic_rejects_inverting_integers() -> None:
	"""
	Check that ~ refuses integers.

	.. versionadded:: 0.1.0
	"""
	integer_values = numpy.array(INTEGERS)
	integers = ArrayLogic._create(integer_values)

	with pytest.raises(IncompatibleTypesError):
		_ = ~integers

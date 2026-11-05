"""
Unit tests of the bounds of an integer result.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

from numdaplot.arrays.operations.integer_bounds import (
	BEYOND_EVERY_INTEGER,
	find_power_bound,
	find_result_bounds,
	find_sum_bounds,
	find_value_bounds,
)

GRID = numpy.array([[1, 2], [-3, 4]])
HUGE_POWER = 10**18


def test_find_value_bounds_gives_python_integers() -> None:
	"""
	Check that the bounds are exact Python integers, which never wrap around.

	.. versionadded:: 0.1.0
	"""
	low_bound, high_bound = find_value_bounds(numpy.array([3, -1], dtype="int8"))

	assert (low_bound, high_bound) == (-1, 3)
	assert type(low_bound) is int
	assert type(high_bound) is int


def test_find_value_bounds_reads_booleans() -> None:
	"""
	Check that booleans count as 0 and 1.

	.. versionadded:: 0.1.0
	"""
	bounds = find_value_bounds(numpy.array([True, False]))

	assert bounds == (0, 1)


@pytest.mark.parametrize(
	("left", "right", "function", "expected_bounds"),
	[
		((-2, 3), (4, 5), numpy.add, (2, 8)),
		((-2, 3), (4, 5), numpy.subtract, (-7, -1)),
		((-2, 3), (4, 5), numpy.multiply, (-10, 15)),
		((-2, 3), (-5, 4), numpy.multiply, (-15, 12)),
		((1, 3), (1, 5), numpy.floor_divide, (0, 3)),
		((-2, 3), (1, 5), numpy.floor_divide, (-3, 3)),
		((1, 3), (-5, -1), numpy.floor_divide, (-3, 3)),
		((1, 3), (0, 2), numpy.power, (0, 9)),
		((-3, 2), (0, 2), numpy.power, (-9, 9)),
	],
)
def test_find_result_bounds_contains_every_result(
	left: tuple[int, int],
	right: tuple[int, int],
	function: numpy.ufunc,
	expected_bounds: tuple[int, int],
) -> None:
	"""
	Check the bounds of each function.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The bounds of the left operand.
	right
		The bounds of the right operand.
	function
		The function.
	expected_bounds
		The expected bounds of the result.
	"""
	bounds = find_result_bounds(left, right, function)

	assert bounds == expected_bounds


@pytest.mark.parametrize(("magnitude", "power", "expected_bound"), [(0, 0, 1), (1, HUGE_POWER, 1), (2, 10, 1024)])
def test_find_power_bound_computes_small_powers(magnitude: int, power: int, expected_bound: int) -> None:
	"""
	Check the bound of small powers, and that 0 and 1 stay small at any power.

	.. versionadded:: 0.1.0

	Parameters
	----------
	magnitude
		The highest absolute value.
	power
		The highest power.
	expected_bound
		The expected bound.
	"""
	bound = find_power_bound(magnitude, power)

	assert bound == expected_bound


def test_find_power_bound_does_not_compute_huge_powers() -> None:
	"""
	Check that a huge power gives a number beyond every type, at once.

	.. versionadded:: 0.1.0
	"""
	bound = find_power_bound(3, HUGE_POWER)

	assert bound == BEYOND_EVERY_INTEGER


def test_find_sum_bounds_of_the_whole_array_counts_every_value() -> None:
	"""
	Check the bounds of the sum of a whole Array.

	.. versionadded:: 0.1.0
	"""
	bounds = find_sum_bounds(GRID, None)

	assert bounds == (-12, 16)


def test_find_sum_bounds_along_an_axis_counts_one_slice() -> None:
	"""
	Check the bounds of the sum of one row.

	.. versionadded:: 0.1.0
	"""
	bounds = find_sum_bounds(GRID, 1)

	assert bounds == (-6, 8)


def test_find_sum_bounds_of_positive_values_starts_at_zero() -> None:
	"""
	Check that positive values have a sum of at least 0, which unsigned types can hold.

	.. versionadded:: 0.1.0
	"""
	bounds = find_sum_bounds(numpy.array([2, 3], dtype="uint8"), None)

	assert bounds == (0, 6)

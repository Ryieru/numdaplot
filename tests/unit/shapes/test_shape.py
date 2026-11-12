"""
Unit tests of Shape.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import pytest

from numdaplot.errors.invalid_shape_error import InvalidShapeError
from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.shapes.shape import Shape

GRID_DIMENSIONS = [3, 4]
EMPTY_DIMENSIONS = [0, 3]
NO_DIMENSION = list[int]()
NEGATIVE_DIMENSIONS = [3, -1]


def test_shape_keeps_its_dimensions() -> None:
	"""
	Check that the dimensions are available as an attribute.

	.. versionadded:: 0.1.0
	"""
	shape = Shape(GRID_DIMENSIONS)

	assert shape.dimensions == GRID_DIMENSIONS


def test_shape_accepts_a_dimension_of_zero() -> None:
	"""
	Check that an empty dimension is accepted.

	.. versionadded:: 0.1.0
	"""
	shape = Shape(EMPTY_DIMENSIONS)

	assert shape.dimensions == EMPTY_DIMENSIONS


def test_shape_rejects_no_dimension() -> None:
	"""
	Check that an empty tuple of dimensions is rejected.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidShapeError):
		Shape(NO_DIMENSION)


def test_shape_rejects_a_negative_dimension() -> None:
	"""
	Check that a negative dimension is rejected.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidShapeError):
		Shape(NEGATIVE_DIMENSIONS)


@pytest.mark.parametrize("dimensions", [(3, 4), 3])
def test_shape_rejects_dimensions_that_are_not_a_list(dimensions: object) -> None:
	"""
	Check that a tuple or a number raises InvalidTypeError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	dimensions
		Dimensions that are not a list.
	"""
	untyped_shape = cast(Any, Shape)

	with pytest.raises(InvalidTypeError):
		untyped_shape(dimensions)


def test_shape_keeps_its_own_copy_of_the_dimensions() -> None:
	"""
	Check that changing the given list afterwards changes nothing.

	.. versionadded:: 0.1.0
	"""
	dimensions = list(GRID_DIMENSIONS)
	shape = Shape(dimensions)

	dimensions.clear()

	assert shape.dimensions == GRID_DIMENSIONS

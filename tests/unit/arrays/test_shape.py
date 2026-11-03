"""
Unit tests of Shape.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.arrays.shape import Shape
from numdaplot.errors.invalid_shape_error import InvalidShapeError

GRID_DIMENSIONS = (3, 4)
EMPTY_DIMENSIONS = (0, 3)
NO_DIMENSION = ()
NEGATIVE_DIMENSIONS = (3, -1)


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

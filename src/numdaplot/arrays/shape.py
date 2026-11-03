"""
Number of values along each dimension of an Array.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

from numdaplot.errors.invalid_shape_error import InvalidShapeError

LOWEST_DIMENSION = 0


@dataclass(frozen=True)
class Shape:
	"""
	Number of values along each dimension of an Array.

	``Shape((3, 4))`` describes 3 rows of 4 values, and ``Shape((5,))`` a single row of 5 values.
	It is used by ``Array.filled``, ``Array.random`` and ``reshape``, and returned by ``Array.shape``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	dimensions
		Number of values along each dimension, at least one dimension and none lower than 0.

	Raises
	------
	InvalidShapeError
		When ``dimensions`` is empty or holds a negative number.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> ndp.Shape((3, 4))
	Shape(dimensions=(3, 4))
	"""

	dimensions: tuple[int, ...]

	def __post_init__(self) -> None:
		"""
		Check that there is at least one dimension and that no dimension is negative.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidShapeError
			When ``dimensions`` is empty or holds a negative number.
		"""
		dimension_count = len(self.dimensions)
		if dimension_count == 0:
			raise InvalidShapeError(self.dimensions)

		for dimension in self.dimensions:
			if dimension < LOWEST_DIMENSION:
				raise InvalidShapeError(self.dimensions)

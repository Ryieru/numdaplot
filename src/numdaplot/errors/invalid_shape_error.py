"""
Error raised when a shape has no dimension or a negative dimension.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_SHAPE_MESSAGE = "Expected at least one dimension and no negative dimension, got {dimensions}."


class InvalidShapeError(NumdaplotError):
	"""
	Raised when a shape has no dimension at all, or a dimension lower than 0.

	.. versionadded:: 0.1.0

	Parameters
	----------
	dimensions
		The rejected dimensions.

	Attributes
	----------
	dimensions
		The rejected dimensions.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Shape((3, -1))
	... except ndp.InvalidShapeError as error:
	... 	print(error)
	Expected at least one dimension and no negative dimension, got (3, -1).
	"""

	def __init__(self, dimensions: tuple[int, ...]) -> None:
		"""
		Build the error message from the dimensions.

		.. versionadded:: 0.1.0

		Parameters
		----------
		dimensions
			The rejected dimensions.
		"""
		message = INVALID_SHAPE_MESSAGE.format(dimensions=dimensions)
		super().__init__(message)

		self.dimensions = dimensions

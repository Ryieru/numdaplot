"""
Error raised when the size of a point cannot be drawn.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_POINT_SIZE_MESSAGE = "Expected a point size above 0, got {point_size}."


class InvalidPointSizeError(NumdaplotError):
	"""
	Raised when the size of a point is 0 or lower, infinite, or not a number.

	.. versionadded:: 0.1.0

	Parameters
	----------
	point_size
		The rejected size.

	Attributes
	----------
	point_size
		The rejected size.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.ScatterChart(point_size=-1.0)
	... except ndp.InvalidPointSizeError as error:
	... 	print(error)
	Expected a point size above 0, got -1.0.
	"""

	def __init__(self, point_size: float) -> None:
		"""
		Build the error message from the size.

		.. versionadded:: 0.1.0

		Parameters
		----------
		point_size
			The rejected size.
		"""
		message = INVALID_POINT_SIZE_MESSAGE.format(point_size=point_size)
		super().__init__(message)

		self.point_size = point_size

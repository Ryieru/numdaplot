"""
Error raised when a size is not positive.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_SIZE_MESSAGE = "Expected a positive width and height, got {width} and {height}."


class InvalidSizeError(NumdaplotError):
	"""
	Raised when the width or the height of a ``Size`` is zero or negative.

	.. versionadded:: 0.1.0

	Parameters
	----------
	width
		The width given.
	height
		The height given.

	Attributes
	----------
	width
		The width given.
	height
		The height given.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> try:
	... 	ndp.Size(width=0, height=4.8)
	... except ndp.InvalidSizeError as error:
	... 	print(error)
	Expected a positive width and height, got 0 and 4.8.
	"""

	def __init__(self, width: float, height: float) -> None:
		"""
		Build the error message from the width and the height.

		.. versionadded:: 0.1.0

		Parameters
		----------
		width
			The width given.
		height
			The height given.
		"""
		message = INVALID_SIZE_MESSAGE.format(width=width, height=height)
		super().__init__(message)
		self.width = width
		self.height = height

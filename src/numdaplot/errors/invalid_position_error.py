"""
Error raised when a position is not a whole number inside its dimension.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_POSITION_MESSAGE = "Expected a whole position between {lowest} and {highest}, got {position}."


class InvalidPositionError(NumdaplotError):
	"""
	Raised when a position is not a whole number, or falls outside its dimension.

	A dimension of size 5 accepts the positions from -5 to 4.

	.. versionadded:: 0.1.0

	Parameters
	----------
	position
		The rejected position.
	size
		Size of the dimension.

	Attributes
	----------
	position
		The rejected position.
	size
		Size of the dimension.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> array = ndp.Array.from_list([1, 2, 3])
	>>> try:
	... 	array.take(ndp.Region(rows=ndp.Index(5)))
	... except ndp.InvalidPositionError as error:
	... 	print(error)
	Expected a whole position between -3 and 2, got 5.
	"""

	def __init__(self, position: float, size: int) -> None:
		"""
		Build the error message from the position and the size.

		.. versionadded:: 0.1.0

		Parameters
		----------
		position
			The rejected position.
		size
			Size of the dimension.
		"""
		lowest_position = -size
		highest_position = size - 1
		message = INVALID_POSITION_MESSAGE.format(lowest=lowest_position, highest=highest_position, position=position)
		super().__init__(message)

		self.position = position
		self.size = size

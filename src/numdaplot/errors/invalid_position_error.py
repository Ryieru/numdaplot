"""
Error raised when a position is not a whole number inside its dimension.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError

INVALID_POSITION_MESSAGE = "Expected a whole position between {lowest} and {highest}, got {position}."
DEFAULT_LOWEST_POSITION = 0
MINIMUM_POSITION_MESSAGE = "Expected a whole position of at least {lowest}, got {position}."


class InvalidPositionError(NumdaplotError):
	"""
	Raised when a position falls outside its dimension.

	A dimension of size 5 accepts the positions from -5 to 4. Without a size, as when an ``Index`` or a ``Cell`` is
	created, the message names the lowest accepted position.

	.. versionadded:: 0.1.0

	Parameters
	----------
	position
		The rejected position.
	size
		Size of the dimension. When omitted, the size is not known yet, as when an ``Index`` is created.
	lowest
		The lowest accepted position, named when the size is not known, 0 by default.

	Attributes
	----------
	position
		The rejected position.
	size
		Size of the dimension, or None.
	lowest
		The lowest accepted position.

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

	def __init__(self, position: object, size: int | None = None, lowest: int = DEFAULT_LOWEST_POSITION) -> None:
		"""
		Build the error message from the position, and the size or the lowest accepted position.

		.. versionadded:: 0.1.0

		Parameters
		----------
		position
			The rejected position.
		size
			Size of the dimension. When omitted, the size is not known yet, as when an ``Index`` is created.
		lowest
			The lowest accepted position, named when the size is not known, 0 by default.
		"""
		message = build_position_message(position, size, lowest)
		super().__init__(message)

		self.position = position
		self.size = size
		self.lowest = lowest


def build_position_message(position: object, size: int | None, lowest: int) -> str:
	"""
	Return the message of a rejected position, naming the accepted positions that are known.

	.. versionadded:: 0.1.0

	Parameters
	----------
	position
		The rejected position.
	size
		Size of the dimension, or None.
	lowest
		The lowest accepted position.

	Returns
	-------
	str
		The message naming the accepted interval, or the lowest accepted position.

	Examples
	--------
	>>> from numdaplot.errors.invalid_position_error import build_position_message
	>>> build_position_message(-1, None, 0)
	'Expected a whole position of at least 0, got -1.'
	"""
	if size is not None:
		highest_position = size - 1
		message = INVALID_POSITION_MESSAGE.format(lowest=-size, highest=highest_position, position=position)
		return message

	return MINIMUM_POSITION_MESSAGE.format(lowest=lowest, position=position)

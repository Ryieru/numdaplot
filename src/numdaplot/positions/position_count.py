"""
Check of the number of positions taken from the start or the end of a dimension.

.. versionadded:: 0.2.0
"""

from numdaplot.errors.invalid_count_error import InvalidCountError

MINIMUM_POSITION_COUNT = 1


def require_position_count(count: int) -> None:
	"""
	Check that a number of positions is 1 or more, a Region always taking something.

	.. versionadded:: 0.2.0

	Parameters
	----------
	count
		The number of positions.

	Raises
	------
	InvalidCountError
		When the number is 0 or negative.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.positions.position_count import require_position_count
	>>> try:
	... 	require_position_count(0)
	... except ndp.InvalidCountError as error:
	... 	print(error)
	Expected a count of at least 1, got 0.
	"""
	if count < MINIMUM_POSITION_COUNT:
		raise InvalidCountError(count, MINIMUM_POSITION_COUNT)

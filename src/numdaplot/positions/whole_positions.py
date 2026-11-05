"""
Check of a position given when an Index or a Cell is created.

.. versionadded:: 0.1.0
"""

from typing import cast

import numpy

from numdaplot.errors.invalid_position_error import InvalidPositionError

WHOLE_NUMBER_TYPES = (int, numpy.integer)


def require_whole_position(position: object, lowest: int | None) -> None:
	"""
	Check that a position is a whole number, and not below the lowest accepted position when there is one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	position
		The position to check.
	lowest
		The lowest accepted position, or None when negative positions count from the end.

	Raises
	------
	InvalidPositionError
		When the position is not a whole number, such as ``1.5`` or ``True``, or is below ``lowest``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.positions.whole_positions import require_whole_position
	>>> require_whole_position(-1, None)
	>>> try:
	... 	require_whole_position(1.5, None)
	... except ndp.InvalidPositionError as error:
	... 	print(error)
	Expected a whole position, got 1.5.
	"""
	is_boolean = isinstance(position, bool)
	if is_boolean:
		raise InvalidPositionError(position, lowest=lowest)

	is_whole_number = isinstance(position, WHOLE_NUMBER_TYPES)
	if not is_whole_number:
		raise InvalidPositionError(position, lowest=lowest)

	if lowest is None:
		return

	# numpy integers compare as Python integers.
	whole_position = cast(int, position)
	if whole_position < lowest:
		raise InvalidPositionError(whole_position, lowest=lowest)

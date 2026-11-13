"""
Check of the number of decimals a number is written with, in a file or in a label.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.settings.invalid_count_error import InvalidCountError

MINIMUM_DECIMAL_COUNT = 0


def require_decimal_count(decimals: int | None) -> None:
	"""
	Check that a number of written decimals, when given, is 0 or more.

	.. versionadded:: 0.1.0

	Parameters
	----------
	decimals
		The number of decimals, or None when every digit is written.

	Raises
	------
	InvalidCountError
		When the number is negative.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.measures.decimal_count import require_decimal_count
	>>> try:
	... 	require_decimal_count(-1)
	... except ndp.InvalidCountError as error:
	... 	print(error)
	Expected a count of at least 0, got -1.
	"""
	if decimals is None:
		return

	if decimals < MINIMUM_DECIMAL_COUNT:
		raise InvalidCountError(decimals, MINIMUM_DECIMAL_COUNT)

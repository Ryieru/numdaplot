"""
Check that a value is a fraction between 0 and 1.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.settings.invalid_fraction_error import InvalidFractionError

MIN_FRACTION = 0.0
MAX_FRACTION = 1.0


def require_fraction(value: float) -> None:
	"""
	Check that a value is a fraction between 0 and 1, both included.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The value to check. NaN is never a fraction.

	Raises
	------
	InvalidFractionError
		When the value is lower than 0, greater than 1 or NaN.

	Examples
	--------
	>>> from numdaplot.measures.fraction import require_fraction
	>>> require_fraction(0.25)
	>>> import numdaplot as ndp
	>>> try:
	... 	require_fraction(-0.1)
	... except ndp.InvalidFractionError as error:
	... 	print(error)
	Expected a fraction between 0 and 1, got -0.1.
	"""
	is_fraction = MIN_FRACTION <= value <= MAX_FRACTION
	if not is_fraction:
		raise InvalidFractionError(value)

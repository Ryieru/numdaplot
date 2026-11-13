"""
Check of the separator of a CSV file.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_separator_error import InvalidSeparatorError

DEFAULT_SEPARATOR = ","
SEPARATOR_LENGTH = 1


def require_separator(separator: str) -> None:
	"""
	Check that the separator of a CSV file is exactly one character.

	.. versionadded:: 0.1.0

	Parameters
	----------
	separator
		The character between two values of a row.

	Raises
	------
	InvalidSeparatorError
		When the separator is empty or longer than one character.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.files.csv.csv_separator import require_separator
	>>> try:
	... 	require_separator(";;")
	... except ndp.InvalidSeparatorError as error:
	... 	print(error)
	Expected a separator of exactly one character, got ';;'.
	"""
	separator_length = len(separator)
	if separator_length != SEPARATOR_LENGTH:
		raise InvalidSeparatorError(separator)

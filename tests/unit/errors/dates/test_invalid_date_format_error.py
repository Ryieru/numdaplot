"""
Unit tests of InvalidDateFormatError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.dates.invalid_date_format_error import InvalidDateFormatError
from numdaplot.errors.numdaplot_error import NumdaplotError

PATTERN = "%d/%m/%Y %z"
EXPECTED_MESSAGE = "Expected a pattern with a date or a time code and no time zone code, got '%d/%m/%Y %z'."


def test_invalid_date_format_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidDateFormatError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidDateFormatError, NumdaplotError)


def test_invalid_date_format_error_message_names_the_pattern() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidDateFormatError(PATTERN)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_date_format_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidDateFormatError(PATTERN)

	assert error.pattern == PATTERN

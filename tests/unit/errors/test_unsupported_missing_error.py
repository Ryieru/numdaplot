"""
Unit tests of UnsupportedMissingError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.unsupported_missing_error import UnsupportedMissingError

TYPE_NAME = "INT64"
EXPECTED_MESSAGE = "INT64 values cannot be missing, use a decimal, date or duration type."


def test_unsupported_missing_error_is_a_numdaplot_error() -> None:
	"""
	Check that UnsupportedMissingError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(UnsupportedMissingError, NumdaplotError)


def test_unsupported_missing_error_message_states_the_problem() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedMissingError(TYPE_NAME)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_unsupported_missing_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = UnsupportedMissingError(TYPE_NAME)

	assert error.type_name == TYPE_NAME

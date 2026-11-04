"""
Unit tests of InvalidBinWidthError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_bin_width_error import InvalidBinWidthError
from numdaplot.errors.numdaplot_error import NumdaplotError

WIDTH = -5.0
EXPECTED_MESSAGE = "Expected a bin width above 0, got -5.0."


def test_invalid_bin_width_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidBinWidthError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidBinWidthError, NumdaplotError)


def test_invalid_bin_width_error_message_states_the_rejected_width() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidBinWidthError(WIDTH)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_bin_width_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidBinWidthError(WIDTH)

	assert error.width == WIDTH

"""
Unit tests of InvalidResolutionError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.files.invalid_resolution_error import InvalidResolutionError
from numdaplot.errors.numdaplot_error import NumdaplotError

DPI = 0
EXPECTED_MESSAGE = "Expected a resolution of at least 1 dot per inch, got 0."


def test_invalid_resolution_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidResolutionError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidResolutionError, NumdaplotError)


def test_invalid_resolution_error_message_states_the_rejected_resolution() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidResolutionError(DPI)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_resolution_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidResolutionError(DPI)

	assert error.dpi == DPI

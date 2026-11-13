"""
Unit tests of InvalidColorError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.plots.invalid_color_error import InvalidColorError

TEXT = "#ff88"
EXPECTED_MESSAGE = "Expected a color written as #rrggbb, got '#ff88'."


def test_invalid_color_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidColorError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidColorError, NumdaplotError)


def test_invalid_color_error_message_states_the_rejected_text() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = InvalidColorError(TEXT)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_color_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = InvalidColorError(TEXT)

	assert error.text == TEXT

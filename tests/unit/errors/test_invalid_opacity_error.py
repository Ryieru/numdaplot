"""
Unit tests of InvalidOpacityError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_opacity_error import InvalidOpacityError
from numdaplot.errors.numdaplot_error import NumdaplotError

OPACITY = 1.5
EXPECTED_MESSAGE = "Expected an opacity above 0 and up to 1, got 1.5."


def test_invalid_opacity_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidOpacityError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidOpacityError, NumdaplotError)


def test_invalid_opacity_error_message_states_the_problem() -> None:
	"""
	Check the message built from the opacity.

	.. versionadded:: 0.1.0
	"""
	error = InvalidOpacityError(OPACITY)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_opacity_error_keeps_the_opacity() -> None:
	"""
	Check that the opacity is available as an attribute.

	.. versionadded:: 0.1.0
	"""
	error = InvalidOpacityError(OPACITY)

	assert error.opacity == OPACITY

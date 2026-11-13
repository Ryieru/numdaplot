"""
Unit tests of InvalidRotationError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.plots.invalid_rotation_error import InvalidRotationError

REJECTED_ROTATION = 120
EXPECTED_MESSAGE = "Expected a rotation from -90 to 90 degrees, got 120."


def test_invalid_rotation_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidRotationError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidRotationError, NumdaplotError)


def test_invalid_rotation_error_names_the_rotation_given() -> None:
	"""
	Check the message and the attribute of the error.

	.. versionadded:: 0.1.0
	"""
	error = InvalidRotationError(REJECTED_ROTATION)

	assert str(error) == EXPECTED_MESSAGE
	assert error.rotation == REJECTED_ROTATION

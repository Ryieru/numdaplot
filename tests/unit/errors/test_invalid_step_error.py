"""
Unit tests of InvalidStepError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.invalid_step_error import InvalidStepError
from numdaplot.errors.numdaplot_error import NumdaplotError

REJECTED_STEP = 0
EXPECTED_MESSAGE = "Expected a non-zero step, got 0."


def test_invalid_step_error_is_a_numdaplot_error() -> None:
	"""
	Check that InvalidStepError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(InvalidStepError, NumdaplotError)


def test_invalid_step_error_message_names_the_rejected_step() -> None:
	"""
	Check that the message states the rejected step.

	.. versionadded:: 0.1.0
	"""
	error = InvalidStepError(REJECTED_STEP)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_invalid_step_error_keeps_the_rejected_step() -> None:
	"""
	Check that the rejected step is available as an attribute.

	.. versionadded:: 0.1.0
	"""
	error = InvalidStepError(REJECTED_STEP)

	assert error.step == REJECTED_STEP

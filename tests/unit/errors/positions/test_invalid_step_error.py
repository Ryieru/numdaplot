"""
Unit tests of InvalidStepError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.positions.invalid_step_error import InvalidStepError

REJECTED_STEP = 0
EXPECTED_MESSAGE = "Expected a non-zero step, got 0."
AWAY_STEP = 1
START = 5
STOP = 1
EXPECTED_DIRECTION_MESSAGE = "Expected a step going from start to stop, got step 1 from 5 to 1."


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


def test_invalid_step_error_names_the_start_and_the_stop_of_a_step_going_away() -> None:
	"""
	Check the message and the attributes for a step going away from the stop.

	.. versionadded:: 0.1.0
	"""
	error = InvalidStepError(AWAY_STEP, START, STOP)

	error_text = str(error)
	assert error_text == EXPECTED_DIRECTION_MESSAGE
	assert error.start == START
	assert error.stop == STOP

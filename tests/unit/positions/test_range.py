"""
Unit tests of Range.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.settings.invalid_step_error import InvalidStepError
from numdaplot.positions.range import DEFAULT_STEP, Range
from numdaplot.rules.bounds import Bounds

START = 0
STOP = 10
DOWNWARD_STEP = -2
ZERO_STEP = 0


def test_range_uses_a_step_of_one_and_included_bounds_by_default() -> None:
	"""
	Check the default step and bounds.

	.. versionadded:: 0.1.0
	"""
	sequence = Range(start=START, stop=STOP)

	assert sequence.step == DEFAULT_STEP
	assert sequence.bounds == Bounds.INCLUDED


def test_range_accepts_a_negative_step() -> None:
	"""
	Check that a range can go downwards.

	.. versionadded:: 0.1.0
	"""
	sequence = Range(start=STOP, stop=START, step=DOWNWARD_STEP)

	assert sequence.step == DOWNWARD_STEP


def test_range_rejects_a_zero_step() -> None:
	"""
	Check that a step of zero is rejected.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidStepError):
		Range(start=START, stop=STOP, step=ZERO_STEP)


@pytest.mark.parametrize(("start", "stop", "step"), [(10, 0, 1), (0, 10, -1)])
def test_range_rejects_a_step_going_away_from_the_stop(start: int, stop: int, step: int) -> None:
	"""
	Check that a step going away from the stop raises InvalidStepError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	start
		The start.
	stop
		The stop, on the other side of the step.
	step
		The step going away.
	"""
	with pytest.raises(InvalidStepError):
		Range(start=start, stop=stop, step=step)


def test_range_accepts_a_start_equal_to_its_stop() -> None:
	"""
	Check that a range of a single number is accepted.

	.. versionadded:: 0.1.0
	"""
	single_range = Range(start=START, stop=START)

	assert single_range.stop == START

"""
Unit tests of Range.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_step_error import InvalidStepError
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

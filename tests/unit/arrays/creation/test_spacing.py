"""
Unit tests of Spacing.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.arrays.creation.spacing import Spacing
from numdaplot.errors.settings.invalid_count_error import InvalidCountError
from numdaplot.rules.bounds import Bounds

START = 0.0
STOP = 1.0
COUNT = 5
SINGLE_COUNT = 1
ZERO_COUNT = 0


def test_spacing_includes_both_bounds_by_default() -> None:
	"""
	Check the default bounds setting.

	.. versionadded:: 0.1.0
	"""
	spacing = Spacing(start=START, stop=STOP, count=COUNT)

	assert spacing.bounds == Bounds.INCLUDED


def test_spacing_rejects_a_single_value_with_both_bounds() -> None:
	"""
	Check that one value cannot be both the start and the stop.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidCountError):
		Spacing(start=START, stop=STOP, count=SINGLE_COUNT)


def test_spacing_accepts_a_single_value_with_one_bound() -> None:
	"""
	Check that one value is accepted when only the start is kept.

	.. versionadded:: 0.1.0
	"""
	spacing = Spacing(start=START, stop=STOP, count=SINGLE_COUNT, bounds=Bounds.LOW_ONLY)

	assert spacing.count == SINGLE_COUNT


def test_spacing_rejects_a_zero_count() -> None:
	"""
	Check that a count of 0 is rejected, whatever the bounds.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidCountError):
		Spacing(start=START, stop=STOP, count=ZERO_COUNT, bounds=Bounds.EXCLUDED)

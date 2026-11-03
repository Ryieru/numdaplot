"""
Unit tests of RandomIntegers and find_drawn_interval.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.arrays.creation.random_integers import RandomIntegers, find_drawn_interval
from numdaplot.errors.invalid_bounds_error import InvalidBoundsError
from numdaplot.rules.bounds import Bounds

DIE_LOW = 1
DIE_HIGH = 6
INCLUDED_INTERVAL = (1, 7)
EXCLUDED_INTERVAL = (2, 6)
LOW_ONLY_INTERVAL = (1, 6)
NEIGHBOUR_LOW = 3
NEIGHBOUR_HIGH = 4


def test_random_integers_include_both_bounds_by_default() -> None:
	"""
	Check the default bounds setting.

	.. versionadded:: 0.1.0
	"""
	distribution = RandomIntegers(low=DIE_LOW, high=DIE_HIGH)

	assert distribution.bounds == Bounds.INCLUDED


def test_random_integers_reject_reversed_bounds() -> None:
	"""
	Check that a low bound greater than the high bound is rejected.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidBoundsError):
		RandomIntegers(low=DIE_HIGH, high=DIE_LOW)


def test_random_integers_reject_an_interval_without_whole_number() -> None:
	"""
	Check that 3 and 4 both excluded leave nothing to draw.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidBoundsError):
		RandomIntegers(low=NEIGHBOUR_LOW, high=NEIGHBOUR_HIGH, bounds=Bounds.EXCLUDED)


def test_find_drawn_interval_extends_an_included_high_bound() -> None:
	"""
	Check that included bounds give the numpy limits 1 and 7 for a die.

	.. versionadded:: 0.1.0
	"""
	distribution = RandomIntegers(low=DIE_LOW, high=DIE_HIGH)

	interval = find_drawn_interval(distribution)

	assert interval == INCLUDED_INTERVAL


def test_find_drawn_interval_moves_an_excluded_low_bound() -> None:
	"""
	Check that excluded bounds give the numpy limits 2 and 6 for 1 to 6.

	.. versionadded:: 0.1.0
	"""
	distribution = RandomIntegers(low=DIE_LOW, high=DIE_HIGH, bounds=Bounds.EXCLUDED)

	interval = find_drawn_interval(distribution)

	assert interval == EXCLUDED_INTERVAL


def test_find_drawn_interval_keeps_an_excluded_high_bound() -> None:
	"""
	Check that LOW_ONLY gives the numpy limits 1 and 6 for 1 to 6.

	.. versionadded:: 0.1.0
	"""
	distribution = RandomIntegers(low=DIE_LOW, high=DIE_HIGH, bounds=Bounds.LOW_ONLY)

	interval = find_drawn_interval(distribution)

	assert interval == LOW_ONLY_INTERVAL

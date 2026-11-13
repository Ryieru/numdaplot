"""
Unit tests of BinCount and BinWidth.

.. versionadded:: 0.1.0
"""

from datetime import timedelta

import pytest

from numdaplot.errors.plots.invalid_bin_width_error import InvalidBinWidthError
from numdaplot.errors.settings.invalid_count_error import InvalidCountError
from numdaplot.plots.charts.bin_count import BinCount
from numdaplot.plots.charts.bin_width import BinWidth

SINGLE_BIN = 1
NO_BIN = 0
SMALL_WIDTH = 0.01
NEGATIVE_WIDTH = -5.0
ZERO_WIDTH = 0.0
HALF_HOUR_DURATION = timedelta(minutes=30)
WHOLE_DAY = timedelta(days=1)
LONGER_THAN_A_DAY = timedelta(hours=25)
ZERO_DURATION = timedelta(0)
NEGATIVE_DURATION = timedelta(minutes=-5)


def test_bin_count_accepts_a_single_bin() -> None:
	"""
	Check that 1 is the smallest number of bins.

	.. versionadded:: 0.1.0
	"""
	bins = BinCount(SINGLE_BIN)

	assert bins.count == SINGLE_BIN


def test_bin_count_rejects_no_bin() -> None:
	"""
	Check that 0 bins raise InvalidCountError at creation.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidCountError):
		BinCount(NO_BIN)


def test_bin_width_accepts_a_small_width() -> None:
	"""
	Check that any width above 0 is accepted.

	.. versionadded:: 0.1.0
	"""
	bins = BinWidth(SMALL_WIDTH)

	assert bins.width == SMALL_WIDTH


@pytest.mark.parametrize("width", [ZERO_WIDTH, NEGATIVE_WIDTH])
def test_bin_width_rejects_a_width_of_zero_or_less(width: float) -> None:
	"""
	Check that a width of 0 or less raises InvalidBinWidthError at creation.

	.. versionadded:: 0.1.0

	Parameters
	----------
	width
		A rejected width.
	"""
	with pytest.raises(InvalidBinWidthError):
		BinWidth(width)


@pytest.mark.parametrize("width", [HALF_HOUR_DURATION, WHOLE_DAY])
def test_bin_width_accepts_a_duration_of_at_most_a_day(width: timedelta) -> None:
	"""
	Check that a duration from above 0 to a whole day is kept.

	.. versionadded:: 0.1.0

	Parameters
	----------
	width
		The duration.
	"""
	bins = BinWidth(width)

	assert bins.width == width


@pytest.mark.parametrize("width", [ZERO_DURATION, NEGATIVE_DURATION, LONGER_THAN_A_DAY])
def test_bin_width_rejects_a_duration_outside_a_day(width: timedelta) -> None:
	"""
	Check that a duration of 0 or less, or beyond a day, raises InvalidBinWidthError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	width
		The duration.
	"""
	with pytest.raises(InvalidBinWidthError):
		BinWidth(width)

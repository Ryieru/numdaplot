"""
Unit tests of compute_range_values.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.creation.range_values import compute_range_values
from numdaplot.positions.range import Range
from numdaplot.rules.bounds import Bounds

INTEGER_RANGE = Range(start=0, stop=10, step=5)
DECIMAL_RANGE = Range(start=0, stop=1, step=0.1)
DOWNWARD_RANGE = Range(start=10, stop=0, step=-3)
SINGLE_EXCLUDED_RANGE = Range(start=1, stop=1, bounds=Bounds.EXCLUDED)
EXCLUDED_RANGE = Range(start=0, stop=3, bounds=Bounds.EXCLUDED)
HIGH_ONLY_RANGE = Range(start=0, stop=3, bounds=Bounds.HIGH_ONLY)
UNREACHED_STOP_RANGE = Range(start=0, stop=10, step=4, bounds=Bounds.LOW_ONLY)
EXPECTED_INTEGERS = [0, 5, 10]
EXPECTED_DECIMAL_COUNT = 11
LAST_DECIMAL = 1.0
EXPECTED_DOWNWARD_VALUES = [10, 7, 4, 1]
EXPECTED_EXCLUDED_VALUES = [1, 2]
EXPECTED_HIGH_ONLY_VALUES = [1, 2, 3]
EXPECTED_UNREACHED_STOP_VALUES = [0, 4, 8]
EMPTY_SIZE = 0


def test_compute_range_values_includes_the_stop_by_default() -> None:
	"""
	Check that an integer range ends on its stop.

	.. versionadded:: 0.1.0
	"""
	values = compute_range_values(INTEGER_RANGE)

	value_list = values.tolist()
	assert value_list == EXPECTED_INTEGERS


def test_compute_range_values_reaches_a_decimal_stop_exactly() -> None:
	"""
	Check that 0 to 1 by 0.1 gives 11 values ending with exactly 1.0, despite rounding errors.

	.. versionadded:: 0.1.0
	"""
	values = compute_range_values(DECIMAL_RANGE)

	last_value = values[-1]
	assert values.size == EXPECTED_DECIMAL_COUNT
	assert last_value == LAST_DECIMAL


def test_compute_range_values_goes_downwards_with_a_negative_step() -> None:
	"""
	Check that a negative step counts down and stops before passing the stop.

	.. versionadded:: 0.1.0
	"""
	values = compute_range_values(DOWNWARD_RANGE)

	value_list = values.tolist()
	assert value_list == EXPECTED_DOWNWARD_VALUES


def test_compute_range_values_is_empty_when_the_excluded_bounds_leave_no_number() -> None:
	"""
	Check that a range from 1 to 1 without its bounds gives no value.

	.. versionadded:: 0.1.0
	"""
	values = compute_range_values(SINGLE_EXCLUDED_RANGE)

	assert values.size == EMPTY_SIZE


def test_compute_range_values_drops_both_excluded_bounds() -> None:
	"""
	Check that EXCLUDED drops the start and the stop.

	.. versionadded:: 0.1.0
	"""
	values = compute_range_values(EXCLUDED_RANGE)

	value_list = values.tolist()
	assert value_list == EXPECTED_EXCLUDED_VALUES


def test_compute_range_values_drops_the_start_with_high_only() -> None:
	"""
	Check that HIGH_ONLY drops the start and keeps the stop.

	.. versionadded:: 0.1.0
	"""
	values = compute_range_values(HIGH_ONLY_RANGE)

	value_list = values.tolist()
	assert value_list == EXPECTED_HIGH_ONLY_VALUES


def test_compute_range_values_keeps_the_last_step_before_an_unreached_stop() -> None:
	"""
	Check that a stop not falling on a step does not shorten the sequence, even when excluded.

	.. versionadded:: 0.1.0
	"""
	values = compute_range_values(UNREACHED_STOP_RANGE)

	value_list = values.tolist()
	assert value_list == EXPECTED_UNREACHED_STOP_VALUES

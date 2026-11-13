"""
Unit tests of build_comparison_mask and build_between_mask.

.. versionadded:: 0.1.0
"""

from datetime import date

import numpy
import pytest

from numdaplot.arrays.array import Array
from numdaplot.arrays.array_data import read_stored_values
from numdaplot.arrays.rules.comparison_masks import (
	build_between_mask,
	build_comparison_mask,
	compare_with_bound,
	read_bound_value,
	require_ordered_bounds,
)
from numdaplot.errors.settings.invalid_bounds_error import InvalidBoundsError
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.rules.between import Between
from numdaplot.rules.bounds import Bounds
from numdaplot.rules.equal import Equal
from numdaplot.rules.greater import Greater
from numdaplot.rules.greater_or_equal import GreaterOrEqual
from numdaplot.rules.less import Less
from numdaplot.rules.less_or_equal import LessOrEqual
from numdaplot.rules.not_equal import NotEqual
from numdaplot.rules.value_rule import ValueRule

ARRAY_PRICES = Array.from_list([10.0, 5.0, None])
TEMPERATURES = numpy.array([18.0, 25.0, 15.0])
LOW_TEMPERATURES = Array.from_list([10.0, 10.0, None])
HIGH_TEMPERATURES = Array.from_list([20.0, 20.0, 20.0])
EXPECTED_IN_RANGE = [True, False, False]
EXPECTED_BELOW_HIGHS = [True, False, True]
REVERSED_LOWS = Array.from_list([10.0, 30.0, None])
REVERSED_HIGHS = Array.from_list([30.0, 5.0, None])
FIXED_HIGH = 20.0
FIXED_LOW = 10.0
EXPECTED_REVERSED_LOW = 30.0
ARRAY_COSTS = Array.from_list([8.0, 7.0, 1.0])
EXPECTED_ABOVE_COSTS = [True, False, False]
VALUES = [1.0, 5.0, 9.0, numpy.nan]
COMPARISONS = [
	(Equal(5.0), [False, True, False, False]),
	(NotEqual(5.0), [True, False, True, False]),
	(Greater(5.0), [False, False, True, False]),
	(GreaterOrEqual(5.0), [False, True, True, False]),
	(Less(5.0), [True, False, False, False]),
	(LessOrEqual(5.0), [True, True, False, False]),
]
INTERVALS = [
	(Between(low=1.0, high=9.0), [True, True, True, False]),
	(Between(low=1.0, high=9.0, bounds=Bounds.EXCLUDED), [False, True, False, False]),
	(Between(low=1.0, high=9.0, bounds=Bounds.LOW_ONLY), [True, True, False, False]),
	(Between(low=1.0, high=9.0, bounds=Bounds.HIGH_ONLY), [False, True, True, False]),
]
DATES = numpy.array(["2026-01-01", "2026-02-01", "NaT"], dtype="datetime64[D]")
DATE_INTERVAL = Between(low=date(2026, 1, 15), high=date(2026, 3, 1))
EXPECTED_DATE_MASK = [False, True, False]
TEXT_RULE = Equal("a")
TEXT_INTERVAL = Between(low="a", high="b")


@pytest.mark.parametrize(("rule", "expected_mask"), COMPARISONS)
def test_build_comparison_mask_applies_each_comparison(rule: ValueRule[float], expected_mask: list[bool]) -> None:
	"""
	Check each comparison rule, a missing value never satisfying it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rule
		A comparison rule.
	expected_mask
		The values satisfying it.
	"""
	values = numpy.array(VALUES)

	mask = build_comparison_mask(values, rule)

	mask_list = mask.tolist()
	assert mask_list == expected_mask


def test_build_comparison_mask_rejects_an_incomparable_reference() -> None:
	"""
	Check that numbers cannot be compared with a text.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(VALUES)

	with pytest.raises(IncompatibleTypesError):
		build_comparison_mask(values, TEXT_RULE)


@pytest.mark.parametrize(("rule", "expected_mask"), INTERVALS)
def test_build_between_mask_follows_the_bounds(rule: Between[float], expected_mask: list[bool]) -> None:
	"""
	Check each bounds setting of an interval, a missing value never being inside.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rule
		An interval rule.
	expected_mask
		The values inside it.
	"""
	values = numpy.array(VALUES)

	mask = build_between_mask(values, rule)

	mask_list = mask.tolist()
	assert mask_list == expected_mask


def test_build_between_mask_compares_dates_with_missing_dates() -> None:
	"""
	Check that a date interval works on dates holding NaT.

	.. versionadded:: 0.1.0
	"""
	mask = build_between_mask(DATES, DATE_INTERVAL)

	mask_list = mask.tolist()
	assert mask_list == EXPECTED_DATE_MASK


def test_build_between_mask_rejects_incomparable_bounds() -> None:
	"""
	Check that numbers cannot be compared with text bounds.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(VALUES)

	with pytest.raises(IncompatibleTypesError):
		build_between_mask(values, TEXT_INTERVAL)


def test_build_comparison_mask_compares_each_value_with_an_array() -> None:
	"""
	Check that an Array as reference compares each value with the value at its position.

	.. versionadded:: 0.2.0
	"""
	price_values = read_stored_values(ARRAY_PRICES)

	mask = build_comparison_mask(price_values, Greater(ARRAY_COSTS))

	mask_list = mask.tolist()
	assert mask_list == EXPECTED_ABOVE_COSTS


def test_build_between_mask_gives_each_value_its_bounds() -> None:
	"""
	Check that bounds given by Arrays apply position by position, a missing bound matching nothing.

	.. versionadded:: 0.2.0
	"""
	mask = build_between_mask(TEMPERATURES, Between(LOW_TEMPERATURES, HIGH_TEMPERATURES))

	mask_list = mask.tolist()
	assert mask_list == EXPECTED_IN_RANGE


def test_compare_with_bound_compares_with_a_single_bound() -> None:
	"""
	Check that a single bound is compared with every value.

	.. versionadded:: 0.2.0
	"""
	below_high = compare_with_bound(TEMPERATURES, FIXED_HIGH, numpy.less_equal)

	below_list = below_high.tolist()
	assert below_list == EXPECTED_BELOW_HIGHS


def test_require_ordered_bounds_rejects_a_low_array_above_its_high_bound() -> None:
	"""
	Check that a low bound given by an Array above the single high bound raises InvalidBoundsError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidBoundsError) as error_info:
		require_ordered_bounds(Between(REVERSED_LOWS, FIXED_HIGH))

	assert error_info.value.low == EXPECTED_REVERSED_LOW


def test_require_ordered_bounds_rejects_a_high_array_below_its_low_bound() -> None:
	"""
	Check that a high bound given by an Array below the single low bound raises InvalidBoundsError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(InvalidBoundsError):
		require_ordered_bounds(Between(FIXED_LOW, REVERSED_HIGHS))


def test_require_ordered_bounds_accepts_ordered_and_missing_bounds() -> None:
	"""
	Check that ordered bounds, and positions with a missing bound, are accepted.

	.. versionadded:: 0.2.0
	"""
	require_ordered_bounds(Between(LOW_TEMPERATURES, HIGH_TEMPERATURES))


def test_read_bound_value_reads_the_bound_at_a_position() -> None:
	"""
	Check that the bound of an Array at a position is a Python value, and a single bound stays itself.

	.. versionadded:: 0.2.0
	"""
	array_bound = read_bound_value(REVERSED_LOWS, 1)
	single_bound = read_bound_value(FIXED_HIGH, 1)

	assert array_bound == EXPECTED_REVERSED_LOW
	assert single_bound == FIXED_HIGH

"""
Unit tests of build_comparison_mask and build_between_mask.

.. versionadded:: 0.1.0
"""

from datetime import date

import numpy
import pytest

from numdaplot.arrays.selection.comparison_masks import build_between_mask, build_comparison_mask
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.rules.between import Between
from numdaplot.rules.bounds import Bounds
from numdaplot.rules.equal import Equal
from numdaplot.rules.greater import Greater
from numdaplot.rules.greater_or_equal import GreaterOrEqual
from numdaplot.rules.less import Less
from numdaplot.rules.less_or_equal import LessOrEqual
from numdaplot.rules.not_equal import NotEqual
from numdaplot.rules.value_rule import ValueRule

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

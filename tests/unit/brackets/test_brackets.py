"""
Unit tests of Brackets.

.. versionadded:: 0.1.0
"""

import math

import pytest

from numdaplot.brackets.bracket_end import BracketEnd
from numdaplot.brackets.brackets import Brackets, require_bracket_labels, require_increasing_limits
from numdaplot.brackets.unmatched import Unmatched
from numdaplot.errors.brackets.invalid_label_count_error import InvalidLabelCountError
from numdaplot.errors.brackets.invalid_limits_error import InvalidLimitsError
from numdaplot.errors.plots.duplicate_label_error import DuplicateLabelError
from numdaplot.errors.settings.empty_list_error import EmptyListError
from numdaplot.errors.settings.refused_setting_error import RefusedSettingError
from numdaplot.rules.bounds import Bounds

AGE_LIMITS = list[int | float]([0, 18, 65])
SINGLE_LIMIT = list[int | float]([0])
NO_LIMIT = list[int | float]()
REPEATED_LIMITS = list[int | float]([0, 10, 10])
DECREASING_LIMITS = list[int | float]([20, 10])
NAN_LIMITS = list[int | float]([0, math.nan])
AGE_LABELS = ["child", "adult", "senior"]
TWO_LABELS = ["child", "adult"]
REPEATED_LABELS = ["child", "child"]
CLOSED_BRACKET_COUNT = 2
BOTH_OPEN_BRACKET_COUNT = 4
SINGLE_OPEN_BRACKET_COUNT = 1


def test_brackets_hold_their_low_limit_and_raise_for_others_by_default() -> None:
	"""
	Check the defaults of the bounds, the ends and others.

	.. versionadded:: 0.1.0
	"""
	brackets = Brackets(limits=AGE_LIMITS)

	assert brackets.bounds == Bounds.LOW_ONLY
	assert brackets.first == BracketEnd.CLOSED
	assert brackets.last == BracketEnd.CLOSED
	assert brackets.others == Unmatched.ERROR
	assert brackets.labels is None


def test_brackets_keep_their_own_copy_of_the_limits() -> None:
	"""
	Check that changing the given list afterwards does not change the brackets.

	.. versionadded:: 0.1.0
	"""
	limits = list(AGE_LIMITS)
	brackets = Brackets(limits=limits)

	limits.append(100)

	assert brackets.limits == AGE_LIMITS


def test_brackets_reject_an_empty_list_of_limits() -> None:
	"""
	Check that brackets need at least one limit.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		Brackets(limits=NO_LIMIT)


@pytest.mark.parametrize("bounds", [Bounds.INCLUDED, Bounds.EXCLUDED])
def test_brackets_refuse_bounds_holding_both_or_no_limit(bounds: Bounds) -> None:
	"""
	Check that INCLUDED and EXCLUDED are refused.

	.. versionadded:: 0.1.0

	Parameters
	----------
	bounds
		A refused member of Bounds.
	"""
	with pytest.raises(RefusedSettingError):
		Brackets(limits=AGE_LIMITS, bounds=bounds)


def test_brackets_refuse_to_keep_unmatched_values() -> None:
	"""
	Check that Unmatched.KEEP is refused, as a number cannot name a bracket.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(RefusedSettingError):
		Brackets(limits=AGE_LIMITS, others=Unmatched.KEEP)


def test_brackets_reject_a_single_limit_without_open_end() -> None:
	"""
	Check that one limit forms no bracket when both ends are closed.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidLimitsError):
		Brackets(limits=SINGLE_LIMIT)


def test_brackets_accept_a_single_limit_with_an_open_end() -> None:
	"""
	Check that one limit and an open last end form one bracket.

	.. versionadded:: 0.1.0
	"""
	brackets = Brackets(limits=SINGLE_LIMIT, last=BracketEnd.OPEN)

	bracket_count = brackets.count_brackets()
	assert bracket_count == SINGLE_OPEN_BRACKET_COUNT


def test_brackets_reject_a_wrong_number_of_labels() -> None:
	"""
	Check that three limits need two labels.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidLabelCountError):
		Brackets(limits=AGE_LIMITS, labels=AGE_LABELS)


def test_brackets_keep_their_labels() -> None:
	"""
	Check that two limits and an open end take three labels.

	.. versionadded:: 0.1.0
	"""
	brackets = Brackets(limits=AGE_LIMITS, labels=AGE_LABELS, last=BracketEnd.OPEN)

	assert brackets.labels == AGE_LABELS


@pytest.mark.parametrize(
	("first", "last", "expected_count"),
	[
		(BracketEnd.CLOSED, BracketEnd.CLOSED, CLOSED_BRACKET_COUNT),
		(BracketEnd.OPEN, BracketEnd.OPEN, BOTH_OPEN_BRACKET_COUNT),
	],
)
def test_count_brackets_adds_one_per_open_end(first: BracketEnd, last: BracketEnd, expected_count: int) -> None:
	"""
	Check the number of brackets of three limits.

	.. versionadded:: 0.1.0

	Parameters
	----------
	first
		The first end.
	last
		The last end.
	expected_count
		The number of brackets.
	"""
	brackets = Brackets(limits=AGE_LIMITS, first=first, last=last)

	bracket_count = brackets.count_brackets()

	assert bracket_count == expected_count


@pytest.mark.parametrize("limits", [REPEATED_LIMITS, DECREASING_LIMITS, NAN_LIMITS])
def test_require_increasing_limits_rejects_limits_not_strictly_increasing(limits: list[int | float]) -> None:
	"""
	Check equal, decreasing and NaN limits.

	.. versionadded:: 0.1.0

	Parameters
	----------
	limits
		Limits that do not strictly increase.
	"""
	with pytest.raises(InvalidLimitsError):
		require_increasing_limits(limits)


def test_require_bracket_labels_rejects_a_label_given_twice() -> None:
	"""
	Check that two equal labels raise DuplicateLabelError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DuplicateLabelError):
		require_bracket_labels(REPEATED_LABELS, CLOSED_BRACKET_COUNT)


def test_require_bracket_labels_accepts_one_label_per_bracket() -> None:
	"""
	Check that distinct labels, one per bracket, raise nothing.

	.. versionadded:: 0.1.0
	"""
	require_bracket_labels(TWO_LABELS, CLOSED_BRACKET_COUNT)

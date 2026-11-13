"""
Unit tests of the names of brackets.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.brackets.bracket_end import BracketEnd
from numdaplot.brackets.bracket_names import (
	Bracket,
	find_first_integer,
	find_last_integer,
	list_brackets,
	write_bracket_names,
	write_decimal_name,
	write_integer_name,
	write_limit,
)
from numdaplot.brackets.brackets import Brackets
from numdaplot.errors.invalid_limits_error import InvalidLimitsError
from numdaplot.rules.bounds import Bounds

LOW = Bounds.LOW_ONLY
HIGH = Bounds.HIGH_ONLY
OPEN = BracketEnd.OPEN
EXPECTED_OPEN_BRACKETS = [Bracket(None, 0), Bracket(0, 10), Bracket(10, None)]
LABELS = ["child", "adult"]
SINGLE_INTEGER_BRACKET = Bracket(5, 6)
EMPTY_INTEGER_BRACKET = Bracket(5.2, 5.8)
HALF_LIMITS = list[int | float]([0.5, 10])
TEN_LIMITS = list[int | float]([0, 10])
AGE_LIMITS = list[int | float]([0, 18, 65])
EMPTY_LIMITS = list[int | float]([5.2, 5.8])
EMPTY_LABELS = ["none"]
EXPECTED_HALF_NAME = "1 to 9"


@pytest.mark.parametrize(
	("bracket", "bounds", "expected_name"),
	[
		(Bracket(0, 10), LOW, "0 to 9"),
		(Bracket(0, 10), HIGH, "1 to 10"),
		(Bracket(5, 6), LOW, "5"),
		(Bracket(80, None), LOW, "80 or more"),
		(Bracket(80, None), HIGH, "81 or more"),
		(Bracket(None, 0), LOW, "-1 or less"),
		(Bracket(None, 0), HIGH, "0 or less"),
	],
)
def test_write_integer_name_gives_the_integers_of_the_bracket(
	bracket: Bracket, bounds: Bounds, expected_name: str
) -> None:
	"""
	Check each integer name of the decided table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	bracket
		A bracket.
	bounds
		The limit each bracket holds.
	expected_name
		The name expected.
	"""
	brackets = Brackets(limits=TEN_LIMITS, bounds=bounds)

	name = write_integer_name(bracket, brackets)

	assert name == expected_name


@pytest.mark.parametrize(
	("bracket", "bounds", "expected_name"),
	[
		(Bracket(0, 10), LOW, "0 to under 10"),
		(Bracket(0, 10), HIGH, "over 0 to 10"),
		(Bracket(80, None), LOW, "80 or more"),
		(Bracket(80, None), HIGH, "over 80"),
		(Bracket(None, 0), LOW, "under 0"),
		(Bracket(None, 0), HIGH, "0 or less"),
	],
)
def test_write_decimal_name_tells_which_limit_the_bracket_holds(
	bracket: Bracket, bounds: Bounds, expected_name: str
) -> None:
	"""
	Check each decimal name of the decided table.

	.. versionadded:: 0.1.0

	Parameters
	----------
	bracket
		A bracket.
	bounds
		The limit each bracket holds.
	expected_name
		The name expected.
	"""
	name = write_decimal_name(bracket, bounds)

	assert name == expected_name


def test_write_integer_name_rejects_a_bracket_without_integer() -> None:
	"""
	Check that a bracket from 5.2 to 5.8 raises InvalidLimitsError.

	.. versionadded:: 0.1.0
	"""
	brackets = Brackets(limits=EMPTY_LIMITS)

	with pytest.raises(InvalidLimitsError):
		write_integer_name(EMPTY_INTEGER_BRACKET, brackets)


def test_write_integer_name_rounds_decimal_limits_inward() -> None:
	"""
	Check that a bracket from 0.5 to 10 holds the integers 1 to 9.

	.. versionadded:: 0.1.0
	"""
	brackets = Brackets(limits=HALF_LIMITS)

	name = write_integer_name(Bracket(0.5, 10), brackets)

	assert name == EXPECTED_HALF_NAME


def test_list_brackets_adds_the_open_ends() -> None:
	"""
	Check the brackets of two limits open on both sides.

	.. versionadded:: 0.1.0
	"""
	brackets = Brackets(limits=TEN_LIMITS, first=OPEN, last=OPEN)

	bracket_list = list_brackets(brackets)

	assert bracket_list == EXPECTED_OPEN_BRACKETS


def test_write_bracket_names_gives_the_labels_when_given() -> None:
	"""
	Check that given labels replace the automatic names.

	.. versionadded:: 0.1.0
	"""
	brackets = Brackets(limits=AGE_LIMITS, labels=LABELS)

	names = write_bracket_names(brackets, True)

	assert names == LABELS


def test_write_bracket_names_checks_integer_brackets_even_with_labels() -> None:
	"""
	Check that an integer bracket without integer is refused even when it has a label.

	.. versionadded:: 0.1.0
	"""
	brackets = Brackets(limits=EMPTY_LIMITS, labels=EMPTY_LABELS)

	with pytest.raises(InvalidLimitsError):
		write_bracket_names(brackets, True)


@pytest.mark.parametrize(("low", "bounds", "expected"), [(10, LOW, 10), (10, HIGH, 11), (0.5, LOW, 1), (0.5, HIGH, 1)])
def test_find_first_integer_rounds_the_low_limit(low: float, bounds: Bounds, expected: int) -> None:
	"""
	Check the first integer of a bracket.

	.. versionadded:: 0.1.0

	Parameters
	----------
	low
		The low limit.
	bounds
		The limit the bracket holds.
	expected
		The first integer.
	"""
	first_integer = find_first_integer(low, bounds)

	assert first_integer == expected


@pytest.mark.parametrize(("high", "bounds", "expected"), [(10, LOW, 9), (10, HIGH, 10), (9.5, LOW, 9), (9.5, HIGH, 9)])
def test_find_last_integer_rounds_the_high_limit(high: float, bounds: Bounds, expected: int) -> None:
	"""
	Check the last integer of a bracket.

	.. versionadded:: 0.1.0

	Parameters
	----------
	high
		The high limit.
	bounds
		The limit the bracket holds.
	expected
		The last integer.
	"""
	last_integer = find_last_integer(high, bounds)

	assert last_integer == expected


@pytest.mark.parametrize(("limit", "expected"), [(10, "10"), (10.0, "10"), (0.1, "0.1"), (-2.5, "-2.5"), (None, "")])
def test_write_limit_writes_whole_limits_without_decimals(limit: float | None, expected: str) -> None:
	"""
	Check the text of each kind of limit.

	.. versionadded:: 0.1.0

	Parameters
	----------
	limit
		A limit or None.
	expected
		Its text.
	"""
	limit_text = write_limit(limit)

	assert limit_text == expected

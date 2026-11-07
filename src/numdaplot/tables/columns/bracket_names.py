"""
Names of brackets written from the values they hold.

.. versionadded:: 0.1.0
"""

import math
from dataclasses import dataclass
from typing import cast

from numdaplot.errors.invalid_limits_error import InvalidLimitsError
from numdaplot.rules.bounds import Bounds
from numdaplot.tables.columns.bracket_end import BracketEnd
from numdaplot.tables.columns.brackets import Brackets

CLOSED_INTEGERS = "{low} to {high}"
INTEGERS_OR_MORE = "{low} or more"
INTEGERS_OR_LESS = "{high} or less"
LOW_DECIMALS = "{low} to under {high}"
HIGH_DECIMALS = "over {low} to {high}"
DECIMALS_OR_MORE = "{low} or more"
OVER_DECIMALS = "over {low}"
UNDER_DECIMALS = "under {high}"
DECIMALS_OR_LESS = "{high} or less"


@dataclass(frozen=True)
class Bracket:
	"""
	One bracket: its low and its high limit, None on an open side.

	.. versionadded:: 0.1.0

	Parameters
	----------
	low
		The low limit, None for an open first bracket.
	high
		The high limit, None for an open last bracket.

	Examples
	--------
	>>> from numdaplot.tables.columns.bracket_names import Bracket
	>>> Bracket(0, 10).high
	10
	"""

	low: int | float | None
	high: int | float | None


def list_brackets(brackets: Brackets) -> list[Bracket]:
	"""
	Return each bracket in order, open ones included.

	.. versionadded:: 0.1.0

	Parameters
	----------
	brackets
		The limits and the open ends.

	Returns
	-------
	list[Bracket]
		One bracket between two limits, an open one before the first limit or after the last one when asked.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.bracket_names import list_brackets
	>>> list_brackets(ndp.Brackets(limits=[0, 10], last=ndp.BracketEnd.OPEN))
	[Bracket(low=0, high=10), Bracket(low=10, high=None)]
	"""
	bracket_list = list[Bracket]()
	limits = brackets.limits
	if brackets.first == BracketEnd.OPEN:
		first_limit = limits[0]
		open_first = Bracket(None, first_limit)
		bracket_list.append(open_first)

	for low, high in zip(limits, limits[1:], strict=False):
		closed_bracket = Bracket(low, high)
		bracket_list.append(closed_bracket)

	if brackets.last == BracketEnd.OPEN:
		last_limit = limits[-1]
		open_last = Bracket(last_limit, None)
		bracket_list.append(open_last)

	return bracket_list


def write_bracket_names(brackets: Brackets, holds_integers: bool) -> list[str]:
	"""
	Return the name of each bracket: the given labels, or the values each bracket holds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	brackets
		The limits, the bounds, the open ends and the labels.
	holds_integers
		Whether the column holds integers, whose names give the first and the last integer of each bracket.

	Returns
	-------
	list[str]
		One name per bracket, in order.

	Raises
	------
	InvalidLimitsError
		When a bracket between two limits holds no integer of a column of integers.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.bracket_names import write_bracket_names
	>>> write_bracket_names(ndp.Brackets(limits=[0, 10, 20], last=ndp.BracketEnd.OPEN), True)
	['0 to 9', '10 to 19', '20 or more']
	>>> write_bracket_names(ndp.Brackets(limits=[0, 10], bounds=ndp.Bounds.HIGH_ONLY), False)
	['over 0 to 10']
	"""
	names = list[str]()
	for bracket in list_brackets(brackets):
		if holds_integers:
			name = write_integer_name(bracket, brackets)
		else:
			name = write_decimal_name(bracket, brackets.bounds)

		names.append(name)

	if brackets.labels is not None:
		return brackets.labels

	return names


def write_integer_name(bracket: Bracket, brackets: Brackets) -> str:
	"""
	Return the name of a bracket of integers: its first and its last integer.

	.. versionadded:: 0.1.0

	Parameters
	----------
	bracket
		The limits of the bracket.
	brackets
		The bounds, and the limits named by the error.

	Returns
	-------
	str
		``0 to 9``, ``5`` for a single integer, ``80 or more`` or ``-1 or less`` for an open bracket.

	Raises
	------
	InvalidLimitsError
		When the bracket holds no integer.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.bracket_names import Bracket, write_integer_name
	>>> write_integer_name(Bracket(0.5, 10), ndp.Brackets(limits=[0.5, 10]))
	'1 to 9'
	"""
	if bracket.low is None:
		# A bracket open on its low side always has a high limit, as Brackets needs a limit or an open end on each side.
		high_limit = cast(int | float, bracket.high)
		last_held = find_last_integer(high_limit, brackets.bounds)
		less_name = INTEGERS_OR_LESS.format(high=last_held)
		return less_name

	first_integer = find_first_integer(bracket.low, brackets.bounds)
	if bracket.high is None:
		more_name = INTEGERS_OR_MORE.format(low=first_integer)
		return more_name

	last_integer = find_last_integer(bracket.high, brackets.bounds)
	if first_integer > last_integer:
		empty_bracket = [bracket.low, bracket.high]
		raise InvalidLimitsError(brackets.limits, empty_bracket)

	if first_integer == last_integer:
		single_name = str(first_integer)
		return single_name

	closed_name = CLOSED_INTEGERS.format(low=first_integer, high=last_integer)

	return closed_name


def find_first_integer(low: int | float, bounds: Bounds) -> int:
	"""
	Return the smallest integer of a bracket from its low limit.

	.. versionadded:: 0.1.0

	Parameters
	----------
	low
		The low limit.
	bounds
		``LOW_ONLY`` when the bracket holds its low limit, ``HIGH_ONLY`` otherwise.

	Returns
	-------
	int
		The low limit rounded up, plus one when the bracket does not hold it and it is a whole number.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.bracket_names import find_first_integer
	>>> find_first_integer(10, ndp.Bounds.LOW_ONLY), find_first_integer(10, ndp.Bounds.HIGH_ONLY)
	(10, 11)
	"""
	if bounds == Bounds.LOW_ONLY:
		held_low = math.ceil(low)
		return held_low

	low_floor = math.floor(low)
	first_integer = low_floor + 1

	return first_integer


def find_last_integer(high: int | float, bounds: Bounds) -> int:
	"""
	Return the largest integer of a bracket from its high limit.

	.. versionadded:: 0.1.0

	Parameters
	----------
	high
		The high limit.
	bounds
		``HIGH_ONLY`` when the bracket holds its high limit, ``LOW_ONLY`` otherwise.

	Returns
	-------
	int
		The high limit rounded down, minus one when the bracket does not hold it and it is a whole number.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.bracket_names import find_last_integer
	>>> find_last_integer(10, ndp.Bounds.LOW_ONLY), find_last_integer(10, ndp.Bounds.HIGH_ONLY)
	(9, 10)
	"""
	if bounds == Bounds.HIGH_ONLY:
		held_high = math.floor(high)
		return held_high

	high_ceiling = math.ceil(high)
	last_integer = high_ceiling - 1

	return last_integer


def write_decimal_name(bracket: Bracket, bounds: Bounds) -> str:
	"""
	Return the name of a bracket of decimals, telling which limit it holds.

	.. versionadded:: 0.1.0

	Parameters
	----------
	bracket
		The limits of the bracket.
	bounds
		``LOW_ONLY`` or ``HIGH_ONLY``.

	Returns
	-------
	str
		``0 to under 10`` or ``over 0 to 10``, and for an open bracket ``80 or more``, ``over 80``, ``under 0`` or
		``0 or less``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.columns.bracket_names import Bracket, write_decimal_name
	>>> write_decimal_name(Bracket(0.5, None), ndp.Bounds.HIGH_ONLY)
	'over 0.5'
	"""
	low_text = write_limit(bracket.low)
	high_text = write_limit(bracket.high)
	holds_low = bounds == Bounds.LOW_ONLY
	if bracket.low is None:
		under_template = UNDER_DECIMALS if holds_low else DECIMALS_OR_LESS
		under_name = under_template.format(high=high_text)
		return under_name

	if bracket.high is None:
		over_template = DECIMALS_OR_MORE if holds_low else OVER_DECIMALS
		over_name = over_template.format(low=low_text)
		return over_name

	closed_template = LOW_DECIMALS if holds_low else HIGH_DECIMALS
	closed_name = closed_template.format(low=low_text, high=high_text)

	return closed_name


def write_limit(limit: int | float | None) -> str:
	"""
	Return a limit with the fewest digits that give it back, a whole number without decimals.

	.. versionadded:: 0.1.0

	Parameters
	----------
	limit
		A limit, or None.

	Returns
	-------
	str
		``10`` for ``10`` or ``10.0``, ``0.1`` for ``0.1``, an empty text for None.

	Examples
	--------
	>>> from numdaplot.tables.columns.bracket_names import write_limit
	>>> write_limit(10.0), write_limit(0.1), write_limit(-3)
	('10', '0.1', '-3')
	"""
	if limit is None:
		return ""

	decimal_limit = float(limit)
	is_whole = decimal_limit.is_integer()
	if is_whole:
		whole_limit = int(limit)
		whole_text = str(whole_limit)
		return whole_text

	shortest_text = repr(limit)

	return shortest_text

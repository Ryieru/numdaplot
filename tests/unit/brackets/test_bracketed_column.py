"""
Unit tests of the conversion of a number column to the categories of its brackets.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
import pytest

from numdaplot.brackets.bracket_end import BracketEnd
from numdaplot.brackets.bracketed_column import cut_column, find_bracket_positions, require_matched_values
from numdaplot.brackets.brackets import Brackets
from numdaplot.brackets.unmatched import Unmatched
from numdaplot.errors.unmatched_value_error import UnmatchedValueError
from numdaplot.rules.bounds import Bounds

AGES = pandas.Series([4, None, 30, 70], dtype="Int64")
AGE_BRACKETS = Brackets(limits=[0, 18, 65], last=BracketEnd.OPEN)
EXPECTED_AGE_NAMES = ["0 to 17", None, "18 to 64", "65 or more"]
EXPECTED_CATEGORIES = ["0 to 17", "18 to 64", "65 or more"]
CATEGORY_DTYPE_NAME = "category"
OUT_OF_BRACKETS = pandas.Series([5, 105], dtype="Int64")
CLOSED_BRACKETS = Brackets(limits=[0, 18, 100])
MISSING_OTHERS = Brackets(limits=[0, 18, 100], others=Unmatched.MISSING)
EXPECTED_MISSING_OTHERS = ["0 to 17", None]
UNMATCHED_VALUE = 105
NUMBERS = numpy.array([-5.0, 0.0, 10.0, 20.0, 25.0, numpy.nan])
LOW_BRACKETS = Brackets(limits=[0, 10, 20], first=BracketEnd.OPEN)
EXPECTED_LOW_POSITIONS = [0, 1, 2, -1, -1, -1]
HIGH_BRACKETS = Brackets(limits=[0, 10, 20], bounds=Bounds.HIGH_ONLY, last=BracketEnd.OPEN)
EXPECTED_HIGH_POSITIONS = [-1, -1, 0, 1, 2, -1]
NO_UNMATCHED = numpy.array([False, False])
SECOND_UNMATCHED = numpy.array([False, True])


def read_names(column: pandas.Series) -> list[str | None]:
	"""
	Return the values of a category column, None where missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A category column.

	Returns
	-------
	list[str or None]
		Its values.
	"""
	raw_names = column.tolist()
	names = [name if isinstance(name, str) else None for name in raw_names]

	return names


def test_cut_column_gives_the_bracket_names_in_bracket_order() -> None:
	"""
	Check the categories, their order and the missing value.

	.. versionadded:: 0.1.0
	"""
	category_column = cut_column(AGES, AGE_BRACKETS)

	names = read_names(category_column)
	category_index = category_column.cat.categories
	categories = category_index.tolist()
	dtype_name = str(category_column.dtype)
	assert dtype_name == CATEGORY_DTYPE_NAME
	assert categories == EXPECTED_CATEGORIES
	assert names == EXPECTED_AGE_NAMES


def test_cut_column_raises_for_a_value_in_no_bracket_by_default() -> None:
	"""
	Check that 105 raises UnmatchedValueError naming it.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(UnmatchedValueError) as error_info:
		cut_column(OUT_OF_BRACKETS, CLOSED_BRACKETS)

	assert error_info.value.value == UNMATCHED_VALUE


def test_cut_column_makes_a_value_in_no_bracket_missing_when_asked() -> None:
	"""
	Check Unmatched.MISSING.

	.. versionadded:: 0.1.0
	"""
	category_column = cut_column(OUT_OF_BRACKETS, MISSING_OTHERS)

	names = read_names(category_column)
	assert names == EXPECTED_MISSING_OTHERS


def test_find_bracket_positions_puts_a_limit_in_the_bracket_above_with_low_only() -> None:
	"""
	Check LOW_ONLY with an open first bracket: 10 is in the bracket from 10 to 20.

	.. versionadded:: 0.1.0
	"""
	positions = find_bracket_positions(NUMBERS, LOW_BRACKETS)

	position_list = positions.tolist()
	assert position_list == EXPECTED_LOW_POSITIONS


def test_find_bracket_positions_puts_a_limit_in_the_bracket_below_with_high_only() -> None:
	"""
	Check HIGH_ONLY with an open last bracket: 10 is in the bracket from 0 to 10.

	.. versionadded:: 0.1.0
	"""
	positions = find_bracket_positions(NUMBERS, HIGH_BRACKETS)

	position_list = positions.tolist()
	assert position_list == EXPECTED_HIGH_POSITIONS


def test_require_matched_values_accepts_values_in_brackets() -> None:
	"""
	Check that no unmatched value raises nothing.

	.. versionadded:: 0.1.0
	"""
	require_matched_values(OUT_OF_BRACKETS, NO_UNMATCHED, Unmatched.ERROR)


def test_require_matched_values_accepts_unmatched_values_made_missing() -> None:
	"""
	Check that Unmatched.MISSING accepts a value in no bracket.

	.. versionadded:: 0.1.0
	"""
	require_matched_values(OUT_OF_BRACKETS, SECOND_UNMATCHED, Unmatched.MISSING)

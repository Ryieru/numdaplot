"""
Unit tests of the masks of columns, conditions and filters.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pandas
import pytest
from numpy.typing import NDArray

from numdaplot.arrays.array import Array
from numdaplot.errors.tables.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.rules.contains import Contains
from numdaplot.rules.greater import Greater
from numdaplot.rules.is_missing import IsMissing
from numdaplot.rules.is_present import IsPresent
from numdaplot.rules.not_equal import NotEqual
from numdaplot.tables.filtering.column_mask import build_column_mask
from numdaplot.tables.filtering.column_match import ColumnMatch
from numdaplot.tables.filtering.condition import Condition
from numdaplot.tables.filtering.filter import Filter
from numdaplot.tables.filtering.filter_mode import FilterMode
from numdaplot.tables.filtering.row_mask import build_condition_mask, build_filter_mask, combine_masks

PRICES = pandas.Series([5, None, 12], dtype="Int64")
EXPECTED_HIGH_PRICES = [False, False, True]
EXPECTED_MISSING_PRICES = [False, True, False]
EXPECTED_PRESENT_PRICES = [True, False, True]
EXPECTED_DIFFERENT_PRICES = [True, False, True]
CITIES = pandas.Series(["Paris", "Lyon"], dtype="category")
EXPECTED_PARIS = [True, False]
FRAME = pandas.DataFrame({"low": [1.0, 5.0, 20.0], "high": [2.0, 30.0, 40.0]})
LIMITS = Array.from_list([4.0, 1.0, 20.0])
EXPECTED_ABOVE_LIMITS = [True, False, False]
EXPECTED_ANY_ABOVE_TEN = [False, True, True]
EXPECTED_ALL_ABOVE_TEN = [False, False, True]
EXPECTED_LOW_ABOVE_TEN = [False, False, True]
EXPECTED_BOTH_CONDITIONS = [False, False, True]
EXPECTED_EITHER_CONDITION = [False, True, True]
TEXT_FRAME = pandas.DataFrame({"city": pandas.Series(["Pau"], dtype="string"), "price": [1.0]})
TRUE_FALSE = numpy.array([True, False])
TRUE_TRUE = numpy.array([True, True])
EXPECTED_EVERY_MASK = [True, False]
EXPECTED_ANY_MASK = [True, True]
EMPTY_MASKS = list[NDArray[numpy.bool_]]()
ROW_COUNT = 2
EXPECTED_NO_MASK_ALL = [True, True]
EXPECTED_NO_MASK_ANY = [False, False]
ABOVE_TEN = Greater(10)
LOW_ABOVE_TEN = Condition(rule=ABOVE_TEN, columns=["low"])
HIGH_ABOVE_TEN = Condition(rule=ABOVE_TEN, columns=["high"])


def read_mask(mask: NDArray[numpy.bool_]) -> list[bool]:
	"""
	Return a mask as a Python list.

	.. versionadded:: 0.1.0

	Parameters
	----------
	mask
		A boolean mask.

	Returns
	-------
	list[bool]
		Its values.
	"""
	raw_mask = mask.tolist()
	mask_list = cast(list[bool], raw_mask)

	return mask_list


@pytest.mark.parametrize(
	("rule", "expected_mask"),
	[
		(ABOVE_TEN, EXPECTED_HIGH_PRICES),
		(IsMissing(), EXPECTED_MISSING_PRICES),
		(IsPresent(), EXPECTED_PRESENT_PRICES),
		(NotEqual(7), EXPECTED_DIFFERENT_PRICES),
	],
)
def test_build_column_mask_lets_missing_values_only_satisfy_is_missing(rule: Any, expected_mask: list[bool]) -> None:
	"""
	Check the mask of each rule on integers with a missing value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rule
		The rule.
	expected_mask
		The rows satisfying it.
	"""
	mask = build_column_mask(PRICES, rule)

	mask_list = read_mask(mask)
	assert mask_list == expected_mask


def test_build_column_mask_reads_categories_as_texts() -> None:
	"""
	Check that a text rule applies to a category column.

	.. versionadded:: 0.1.0
	"""
	mask = build_column_mask(CITIES, Contains("Par"))

	mask_list = read_mask(mask)
	assert mask_list == EXPECTED_PARIS


@pytest.mark.parametrize(
	("mode", "expected_mask"),
	[
		(ColumnMatch.ANY, EXPECTED_ANY_ABOVE_TEN),
		(ColumnMatch.ALL, EXPECTED_ALL_ABOVE_TEN),
	],
)
def test_build_condition_mask_combines_every_column(mode: ColumnMatch, expected_mask: list[bool]) -> None:
	"""
	Check that a condition without columns applies to every column, with any or all of them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	mode
		How the columns combine.
	expected_mask
		The rows satisfying the condition.
	"""
	condition = Condition(rule=ABOVE_TEN, mode=mode)

	mask = build_condition_mask(FRAME, condition)

	mask_list = read_mask(mask)
	assert mask_list == expected_mask


def test_build_condition_mask_applies_to_the_named_columns() -> None:
	"""
	Check that only the named column is checked.

	.. versionadded:: 0.1.0
	"""
	mask = build_condition_mask(FRAME, LOW_ABOVE_TEN)

	mask_list = read_mask(mask)
	assert mask_list == EXPECTED_LOW_ABOVE_TEN


def test_build_condition_mask_rejects_an_unknown_column() -> None:
	"""
	Check that an unknown column raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	condition = Condition(rule=ABOVE_TEN, columns=["prise"])

	with pytest.raises(ColumnNotFoundError):
		build_condition_mask(FRAME, condition)


def test_build_condition_mask_rejects_a_rule_that_does_not_apply_to_a_column() -> None:
	"""
	Check that a number rule over every column, a text column included, raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	condition = Condition(rule=ABOVE_TEN)

	with pytest.raises(IncompatibleTypesError):
		build_condition_mask(TEXT_FRAME, condition)


@pytest.mark.parametrize(
	("mode", "expected_mask"),
	[
		(FilterMode.ALL, EXPECTED_BOTH_CONDITIONS),
		(FilterMode.ANY, EXPECTED_EITHER_CONDITION),
	],
)
def test_build_filter_mask_combines_the_conditions(mode: FilterMode, expected_mask: list[bool]) -> None:
	"""
	Check that conditions combine with all or any.

	.. versionadded:: 0.1.0

	Parameters
	----------
	mode
		How the conditions combine.
	expected_mask
		The kept rows.
	"""
	row_filter = Filter(conditions=[LOW_ABOVE_TEN, HIGH_ABOVE_TEN], mode=mode)

	mask = build_filter_mask(FRAME, row_filter)

	mask_list = read_mask(mask)
	assert mask_list == expected_mask


@pytest.mark.parametrize(
	("requires_all", "expected_mask"),
	[
		(True, EXPECTED_EVERY_MASK),
		(False, EXPECTED_ANY_MASK),
	],
)
def test_combine_masks_keeps_every_or_any_mask(requires_all: bool, expected_mask: list[bool]) -> None:
	"""
	Check the combination of two masks.

	.. versionadded:: 0.1.0

	Parameters
	----------
	requires_all
		Whether every mask is required.
	expected_mask
		The combined mask.
	"""
	mask = combine_masks([TRUE_FALSE, TRUE_TRUE], requires_all, ROW_COUNT)

	mask_list = read_mask(mask)
	assert mask_list == expected_mask


@pytest.mark.parametrize(
	("requires_all", "expected_mask"),
	[
		(True, EXPECTED_NO_MASK_ALL),
		(False, EXPECTED_NO_MASK_ANY),
	],
)
def test_combine_masks_handles_no_mask(requires_all: bool, expected_mask: list[bool]) -> None:
	"""
	Check that no mask keeps every row with all, and no row with any.

	.. versionadded:: 0.1.0

	Parameters
	----------
	requires_all
		Whether every mask is required.
	expected_mask
		The combined mask.
	"""
	mask = combine_masks(EMPTY_MASKS, requires_all, ROW_COUNT)

	mask_list = read_mask(mask)
	assert mask_list == expected_mask


def test_build_column_mask_compares_each_row_with_an_array() -> None:
	"""
	Check that an Array as reference is followed row by row, the missing value of the column matching nothing.

	.. versionadded:: 0.2.0
	"""
	mask = build_column_mask(PRICES, Greater(LIMITS))

	mask_list = mask.tolist()
	assert mask_list == EXPECTED_ABOVE_LIMITS

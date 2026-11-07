"""
Functional tests of number columns cut into brackets.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp

AGES = [4, 17, 30, 92]
AGE_BRACKETS = ndp.Brackets(limits=[0, 10, 20], last=ndp.BracketEnd.OPEN)
EXPECTED_AGE_NAMES = ["0 to 9", "10 to 19", "20 or more", "20 or more"]
LIFE_AGES = [70, 30, 5]
LIFE_BRACKETS = ndp.Brackets(limits=[0, 18, 65], labels=["young", "adult", "old"], last=ndp.BracketEnd.OPEN)
EXPECTED_LIFE_ORDER = ["young", "adult", "old"]
WIDTHS = [0.0, 2.5, 10.0, 12.0]
WIDTH_BRACKETS = ndp.Brackets(limits=[0, 2.5, 10], bounds=ndp.Bounds.HIGH_ONLY, last=ndp.BracketEnd.OPEN)
EXPECTED_WIDTH_NAMES = [None, "over 0 to 2.5", "over 2.5 to 10", "over 10"]
WIDTH_MISSING_BRACKETS = ndp.Brackets(
	limits=[0, 2.5, 10], bounds=ndp.Bounds.HIGH_ONLY, last=ndp.BracketEnd.OPEN, others=ndp.Unmatched.MISSING
)
OLD_AGES = [5, 105]
CLOSED_AGE_BRACKETS = ndp.Brackets(limits=[0, 18, 100])
EXPECTED_UNMATCHED_MESSAGE = (
	"The value 105 is in no bracket. Open the first or the last bracket, or give others=Unmatched.MISSING to make it "
	"missing."
)
ROADS = ["A1", "N7"]


def cut(values: list[int] | list[float], brackets: ndp.Brackets) -> ndp.Table:
	"""
	Return a Table of one column named value, converted to the categories of brackets.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The numbers of the column.
	brackets
		The brackets.

	Returns
	-------
	ndp.Table
		The converted Table.
	"""
	numbers = ndp.Array.from_list(values)
	table = ndp.Table.from_arrays({"value": numbers})
	conversion = ndp.Conversion(column="value", dtype=ndp.Type.CATEGORY, format=brackets)
	cut_table = table.convert(conversion)

	return cut_table


def test_ages_are_cut_into_named_brackets() -> None:
	"""
	Check the automatic names of integer brackets with an open last one.

	.. versionadded:: 0.1.0
	"""
	cut_table = cut(AGES, AGE_BRACKETS)

	value_column = cut_table.column("value")
	names = value_column.to_list()
	assert cut_table.column_types["value"] == ndp.Type.CATEGORY
	assert names == EXPECTED_AGE_NAMES


def test_sorting_and_grouping_follow_the_order_of_the_brackets() -> None:
	"""
	Check that given labels keep the order of the brackets, not the alphabetical one.

	.. versionadded:: 0.1.0
	"""
	cut_table = cut(LIFE_AGES, LIFE_BRACKETS)
	count = ndp.Calculation(column="value", function=ndp.Count())

	sorted_table = cut_table.sort(ndp.Sorting(keys=[ndp.SortKey(column="value")]))
	counts = cut_table.aggregate(ndp.Aggregation(calculations=[count], group_by=["value"]))

	sorted_column = sorted_table.column("value")
	group_column = counts.column("value")
	sorted_names = sorted_column.to_list()
	group_names = group_column.to_list()
	assert sorted_names == EXPECTED_LIFE_ORDER
	assert group_names == EXPECTED_LIFE_ORDER


def test_a_decimal_outside_the_brackets_is_named_in_the_error() -> None:
	"""
	Check that 0.0 is in no bracket holding its high limit, and that MISSING makes it missing.

	.. versionadded:: 0.1.0
	"""
	missing_table = cut(WIDTHS, WIDTH_MISSING_BRACKETS)

	with pytest.raises(ndp.UnmatchedValueError):
		cut(WIDTHS, WIDTH_BRACKETS)

	value_column = missing_table.column("value")
	names = value_column.to_list()
	assert names == EXPECTED_WIDTH_NAMES


def test_a_value_above_the_last_limit_points_to_an_open_bracket() -> None:
	"""
	Check the message of a value in no bracket.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.UnmatchedValueError) as error_info:
		cut(OLD_AGES, CLOSED_AGE_BRACKETS)

	error_text = str(error_info.value)
	assert error_text == EXPECTED_UNMATCHED_MESSAGE


def test_brackets_are_refused_on_texts() -> None:
	"""
	Check that brackets given to a text column raise InvalidConversionError.

	.. versionadded:: 0.1.0
	"""
	road_names = ndp.Array.from_list(ROADS)
	roads = ndp.Table.from_arrays({"road": road_names})
	conversion = ndp.Conversion(column="road", dtype=ndp.Type.CATEGORY, format=AGE_BRACKETS)

	with pytest.raises(ndp.InvalidConversionError):
		roads.convert(conversion)

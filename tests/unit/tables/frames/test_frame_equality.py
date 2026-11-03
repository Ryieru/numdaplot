"""
Unit tests of the comparison of Table columns.

.. versionadded:: 0.1.0
"""

import pandas

from numdaplot.arrays.type_match import TypeMatch
from numdaplot.tables.frames.frame_equality import are_columns_equal, are_frames_equal

INTEGER_PRICES = pandas.DataFrame({"price": pandas.Series([1, None], dtype="Int64")})
DECIMAL_PRICES = pandas.DataFrame({"price": [1.0, None]})
RENAMED_PRICES = pandas.DataFrame({"cost": [1.0, None]})
LONGER_PRICES = pandas.DataFrame({"price": [1.0, None, 3.0]})
TWO_COLUMNS = pandas.DataFrame({"a": [1.0], "b": [2.0]})
SWAPPED_COLUMNS = pandas.DataFrame({"b": [2.0], "a": [1.0]})
DECIMALS = pandas.Series([1.5, None])
SAME_DECIMALS = pandas.Series([1.5, None])
OTHER_DECIMALS = pandas.Series([2.5, None])
MOVED_MISSING = pandas.Series([None, 1.5])
TEXTS = pandas.Series(["1.5", None], dtype="string")
TEXT_CATEGORIES = pandas.Series(["a", "b"], dtype="category")
TEXTS_OF_CATEGORIES = pandas.Series(["a", "b"], dtype="string")


def test_are_frames_equal_ignores_the_types_by_default() -> None:
	"""
	Check that integers and decimals of the same values are equal with TypeMatch.IGNORED.

	.. versionadded:: 0.1.0
	"""
	is_equal = are_frames_equal(INTEGER_PRICES, DECIMAL_PRICES, TypeMatch.IGNORED)

	assert is_equal


def test_are_frames_equal_compares_the_types_when_strict() -> None:
	"""
	Check that integers and decimals differ with TypeMatch.STRICT.

	.. versionadded:: 0.1.0
	"""
	is_equal = are_frames_equal(INTEGER_PRICES, DECIMAL_PRICES, TypeMatch.STRICT)

	assert not is_equal


def test_are_frames_equal_compares_the_column_names() -> None:
	"""
	Check that a renamed column makes the Tables different.

	.. versionadded:: 0.1.0
	"""
	is_equal = are_frames_equal(DECIMAL_PRICES, RENAMED_PRICES, TypeMatch.IGNORED)

	assert not is_equal


def test_are_frames_equal_compares_the_order_of_the_columns() -> None:
	"""
	Check that swapped columns make the Tables different.

	.. versionadded:: 0.1.0
	"""
	is_equal = are_frames_equal(TWO_COLUMNS, SWAPPED_COLUMNS, TypeMatch.IGNORED)

	assert not is_equal


def test_are_frames_equal_compares_the_number_of_rows() -> None:
	"""
	Check that a Table with one more row is different.

	.. versionadded:: 0.1.0
	"""
	is_equal = are_frames_equal(DECIMAL_PRICES, LONGER_PRICES, TypeMatch.IGNORED)

	assert not is_equal


def test_are_columns_equal_treats_two_missing_values_as_equal() -> None:
	"""
	Check that missing values at the same rows are equal.

	.. versionadded:: 0.1.0
	"""
	is_equal = are_columns_equal(DECIMALS, SAME_DECIMALS, TypeMatch.STRICT)

	assert is_equal


def test_are_columns_equal_compares_the_present_values() -> None:
	"""
	Check that a different value makes the columns different.

	.. versionadded:: 0.1.0
	"""
	is_equal = are_columns_equal(DECIMALS, OTHER_DECIMALS, TypeMatch.IGNORED)

	assert not is_equal


def test_are_columns_equal_compares_the_rows_of_the_missing_values() -> None:
	"""
	Check that missing values at different rows make the columns different.

	.. versionadded:: 0.1.0
	"""
	is_equal = are_columns_equal(DECIMALS, MOVED_MISSING, TypeMatch.IGNORED)

	assert not is_equal


def test_are_columns_equal_never_matches_numbers_and_texts() -> None:
	"""
	Check that a number and its text are not equal.

	.. versionadded:: 0.1.0
	"""
	is_equal = are_columns_equal(DECIMALS, TEXTS, TypeMatch.IGNORED)

	assert not is_equal


def test_are_columns_equal_matches_categories_and_texts_of_the_same_values() -> None:
	"""
	Check that categories and texts belong to the same family.

	.. versionadded:: 0.1.0
	"""
	is_equal = are_columns_equal(TEXT_CATEGORIES, TEXTS_OF_CATEGORIES, TypeMatch.IGNORED)

	assert is_equal

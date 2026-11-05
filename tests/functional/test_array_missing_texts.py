"""
Functional tests of missing texts in an Array.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pandas
import pytest

import numdaplot as ndp

TEXTS_WITH_HOLE = ["b", None, "a", "b"]
MISSING_ONLY = [None, None]
# Some versions of the numpy stubs leave out the missing value marker of StringDType.
STRING_DTYPE_CLASS = cast(Any, numpy.dtypes.StringDType)
TEXT_DTYPE_MARKED_WITH_NONE = STRING_DTYPE_CLASS(na_object=None)
COLUMN_NAME = "payment"


def build_texts() -> ndp.Array:
	"""
	Return an Array of texts with one missing value.

	.. versionadded:: 0.1.0

	Returns
	-------
	Array
		The values ``b``, missing, ``a`` and ``b``.
	"""
	texts = ndp.Array.from_list(TEXTS_WITH_HOLE)

	return texts


def build_table(dtype: str) -> ndp.Table:
	"""
	Return a Table with one column holding a missing value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	dtype
		The pandas dtype of the column.

	Returns
	-------
	Table
		The Table.
	"""
	column = pandas.Series(TEXTS_WITH_HOLE, dtype=dtype)
	frame = pandas.DataFrame({COLUMN_NAME: column})
	table = ndp.Table.from_pandas(frame)

	return table


def test_from_list_gives_back_none_for_a_missing_text() -> None:
	"""
	Check that a list with None comes back unchanged from the Array.

	.. versionadded:: 0.1.0
	"""
	texts = build_texts()

	python_values = texts.to_list()

	assert python_values == TEXTS_WITH_HOLE


def test_nested_lists_give_back_none_for_a_missing_text() -> None:
	"""
	Check that nested lists come back unchanged from the Array.

	.. versionadded:: 0.1.0
	"""
	nested_values: list[Any] = [["a", None], ["b", "c"]]
	texts = ndp.Array.from_list(nested_values)

	python_values = texts.to_list()

	assert python_values == nested_values


def test_to_value_gives_none_for_a_single_missing_text() -> None:
	"""
	Check that the single value of an Array is None when it is a missing text.

	.. versionadded:: 0.1.0
	"""
	single_text = ndp.Array.from_list([None], dtype=ndp.Type.TEXT)

	python_value = single_text.to_value()

	assert python_value is None


def test_a_missing_text_shows_as_nan() -> None:
	"""
	Check that an Array shows a missing text as nan, like a missing decimal.

	.. versionadded:: 0.1.0
	"""
	texts = build_texts()

	shown_text = repr(texts)

	assert shown_text == "Array(['b', nan, 'a', 'b'], dtype=TEXT)"


def test_the_text_nan_is_not_a_missing_value() -> None:
	"""
	Check that the text ``nan`` stays different from a missing text, in an Array and in a Table.

	.. versionadded:: 0.1.0
	"""
	texts = ndp.Array.from_list(["nan", None])
	table = ndp.Table.from_arrays({COLUMN_NAME: texts})

	missing = texts.check(ndp.IsMissing())
	missing_list = missing.to_list()
	missing_count = table.count_missing().to_value()
	python_values = table.column(COLUMN_NAME).to_list()

	assert missing_list == [False, True]
	assert missing_count == 1
	assert python_values == ["nan", None]


@pytest.mark.parametrize("dtype", ["string", "category"])
def test_column_keeps_every_row_with_missing_texts(dtype: str) -> None:
	"""
	Check that a text or category column gives one value per row, its missing value included.

	.. versionadded:: 0.1.0

	Parameters
	----------
	dtype
		The pandas dtype of the column.
	"""
	table = build_table(dtype)

	column = table.column(COLUMN_NAME)

	python_values = column.to_list()
	assert python_values == TEXTS_WITH_HOLE
	assert column.dtype == ndp.Type.TEXT


def test_a_column_with_missing_texts_goes_back_into_a_table() -> None:
	"""
	Check that the Array of a column gives the same column when added back.

	.. versionadded:: 0.1.0
	"""
	table = build_table("string")
	column = table.column(COLUMN_NAME)

	new_table = ndp.Table.from_arrays({COLUMN_NAME: column})

	is_equal = new_table.is_equal(ndp.Equality(other=table))
	assert is_equal


def test_adding_texts_keeps_a_missing_text_missing() -> None:
	"""
	Check that adding a text to a missing text gives a missing text.

	.. versionadded:: 0.1.0
	"""
	texts = build_texts()

	joined_texts = texts + "x"

	python_values = joined_texts.to_list()
	assert python_values == ["bx", None, "ax", "bx"]


@pytest.mark.parametrize(
	("sorting", "expected_values"),
	[
		(ndp.ArraySorting(), ["a", "b", "b", None]),
		(ndp.ArraySorting(order=ndp.Order.DESCENDING), ["b", "b", "a", None]),
		(ndp.ArraySorting(missing=ndp.MissingPosition.FIRST), [None, "a", "b", "b"]),
	],
)
def test_sort_places_a_missing_text_with_the_setting(sorting: ndp.ArraySorting, expected_values: list[Any]) -> None:
	"""
	Check that a sort of texts follows its order and its position of the missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	sorting
		The sort settings.
	expected_values
		The sorted values.
	"""
	texts = build_texts()

	sorted_texts = texts.sort(sorting)

	python_values = sorted_texts.to_list()
	assert python_values == expected_values


def test_unique_keeps_one_missing_text_last() -> None:
	"""
	Check that unique gives the missing value once, after the present values.

	.. versionadded:: 0.1.0
	"""
	texts = build_texts()

	unique_texts = texts.unique()

	python_values = unique_texts.to_list()
	assert python_values == ["a", "b", None]


@pytest.mark.parametrize(
	("statistic", "expected_value"),
	[
		(ndp.Count(), 3),
		(ndp.Count(missing=ndp.CountedMissing.INCLUDED), 4),
		(ndp.Min(), "a"),
		(ndp.Max(), "b"),
		(ndp.MostFrequent(), "b"),
	],
)
def test_statistics_handle_a_missing_text(statistic: ndp.Statistic, expected_value: object) -> None:
	"""
	Check that the statistics accepting texts ignore a missing text, unless asked to count it.

	.. versionadded:: 0.1.0

	Parameters
	----------
	statistic
		The statistic.
	expected_value
		Its result.
	"""
	texts = build_texts()

	result = texts.compute(statistic)

	result_value = result.to_value()
	assert result_value == expected_value


def test_max_without_any_present_text_is_refused() -> None:
	"""
	Check that Max has no result without a present text.

	.. versionadded:: 0.1.0
	"""
	texts = ndp.Array.from_list(MISSING_ONLY, dtype=ndp.Type.TEXT)

	with pytest.raises(ndp.EmptyArrayError):
		texts.compute(ndp.Max())


@pytest.mark.parametrize(
	("rule", "expected_mask"),
	[
		(ndp.IsMissing(), [False, True, False, False]),
		(ndp.IsPresent(), [True, False, True, True]),
		(ndp.Equal("b"), [True, False, False, True]),
		(ndp.NotEqual("b"), [False, False, True, False]),
		(ndp.Greater("a"), [True, False, False, True]),
		(ndp.Less("b"), [False, False, True, False]),
		(ndp.Between("a", "b"), [True, False, True, True]),
		(ndp.IsIn(["b"]), [True, False, False, True]),
		(ndp.Contains("b"), [True, False, False, True]),
		(ndp.Contains("B", case=ndp.Case.IGNORED), [True, False, False, True]),
	],
)
def test_a_missing_text_only_satisfies_is_missing(rule: ndp.Rule, expected_mask: list[bool]) -> None:
	"""
	Check every rule accepting texts on a missing text.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rule
		The rule.
	expected_mask
		The expected result of the check.
	"""
	texts = build_texts()

	mask = texts.check(rule)

	mask_values = mask.to_list()
	assert mask_values == expected_mask


def test_take_keeps_a_missing_text() -> None:
	"""
	Check that a region holding a missing text keeps it.

	.. versionadded:: 0.1.0
	"""
	texts = build_texts()

	region = ndp.Region(rows=ndp.Range(start=0, stop=1))
	first_texts = texts.take(region)

	python_values = first_texts.to_list()
	assert python_values == ["b", None]


def test_replace_fills_a_missing_text() -> None:
	"""
	Check that a replacement writes a text over a missing text.

	.. versionadded:: 0.1.0
	"""
	texts = build_texts()

	region = ndp.Region(rows=ndp.Index(1))
	filled_texts = texts.replace(ndp.Replacement(region=region, value="z"))

	python_values = filled_texts.to_list()
	assert python_values == ["b", "z", "a", "b"]


def test_is_equal_reads_two_missing_texts_as_equal() -> None:
	"""
	Check that two Arrays with a missing text at the same position are equal.

	.. versionadded:: 0.1.0
	"""
	texts = build_texts()
	same_texts = build_texts()

	is_equal = texts.is_equal(ndp.Equality(other=same_texts))

	assert is_equal


def test_from_numpy_reads_another_missing_marker() -> None:
	"""
	Check that a numpy text array marking missing values with None gives a usable Array.

	.. versionadded:: 0.1.0
	"""
	marked_values = numpy.array(["b", None, "a"], dtype=TEXT_DTYPE_MARKED_WITH_NONE)

	texts = ndp.Array.from_numpy(marked_values)
	sorted_texts = texts.sort()

	python_values = sorted_texts.to_list()
	assert python_values == ["a", "b", None]


@pytest.mark.parametrize(
	("values", "expected_message"),
	[
		([1, None], "INT64 values cannot be missing in an Array. Remove them, or give dtype=ndp.Type.FLOAT64."),
		([True, None], "BOOL values cannot be missing in an Array. Remove them."),
	],
)
def test_from_list_refuses_missing_integers_and_booleans(values: list[Any], expected_message: str) -> None:
	"""
	Check the refusal of a missing integer or boolean, and its advice.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values given.
	expected_message
		The message of the error.
	"""
	with pytest.raises(ndp.UnsupportedMissingError) as error_info:
		ndp.Array.from_list(values)

	error_text = str(error_info.value)
	assert error_text == expected_message


def test_the_advice_for_missing_integers_works() -> None:
	"""
	Check that giving FLOAT64, as the message advises, accepts a missing integer.

	.. versionadded:: 0.1.0
	"""
	decimals = ndp.Array.from_list([1, None], dtype=ndp.Type.FLOAT64)

	missing = decimals.check(ndp.IsMissing())
	missing_list = missing.to_list()

	assert missing_list == [False, True]


@pytest.mark.parametrize(
	("dtype", "values", "expected_message"),
	[
		(
			"Int64",
			[1, None],
			"The column 'payment' has missing values, which an INT64 Array cannot hold. "
			"Remove them with drop_missing, or convert the column to FLOAT64.",
		),
		(
			"boolean",
			[True, None],
			"The column 'payment' has missing values, which a BOOL Array cannot hold. Remove them with drop_missing.",
		),
	],
)
def test_column_refuses_missing_integers_and_booleans(dtype: str, values: list[Any], expected_message: str) -> None:
	"""
	Check the refusal of an integer or boolean column with a missing value, and its advice.

	.. versionadded:: 0.1.0

	Parameters
	----------
	dtype
		The pandas dtype of the column.
	values
		The values of the column.
	expected_message
		The message of the error.
	"""
	column = pandas.Series(values, dtype=dtype)
	frame = pandas.DataFrame({COLUMN_NAME: column})
	table = ndp.Table.from_pandas(frame)

	with pytest.raises(ndp.UnsupportedMissingError) as error_info:
		table.column(COLUMN_NAME)

	error_text = str(error_info.value)
	assert error_text == expected_message

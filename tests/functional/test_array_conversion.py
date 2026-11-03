"""
Functional tests of the conversion and comparison of Arrays.

.. versionadded:: 0.1.0
"""

from datetime import datetime

import numpy
import pytest

import numdaplot as ndp

GRID = [[1, 2], [3, 4]]
PRICES = [10, 20]
PRICE = 10
SINGLE_PRICE = [PRICE]
INTEGERS = [1, 2]
DECIMALS = [1.0, 2.0]
TEMPERATURES = [12.0, None]
MOMENTS = [datetime(2026, 1, 31, 8, 30), None]
EXPECTED_PRICES_TEXT = "Array([10, 20], dtype=INT64)"
CHANGED_PRICE = 99
FIRST_POSITION = 0
COMPLEX_VALUES = [1j]


def test_a_grid_is_read_as_nested_lists() -> None:
	"""
	Check that to_list gives one list per row.

	.. versionadded:: 0.1.0
	"""
	grid = ndp.Array.from_list(GRID)

	grid_rows = grid.to_list()

	assert grid_rows == GRID


def test_datetimes_are_read_back_as_python_datetimes() -> None:
	"""
	Check that datetimes and a missing datetime come back as given.

	.. versionadded:: 0.1.0
	"""
	moments = ndp.Array.from_list(MOMENTS)

	moment_list = moments.to_list()

	assert moment_list == MOMENTS


def test_a_single_value_is_read_as_a_python_value() -> None:
	"""
	Check that to_value gives the price itself.

	.. versionadded:: 0.1.0
	"""
	single_price = ndp.Array.from_list(SINGLE_PRICE)

	price = single_price.to_value()

	assert price == PRICE


def test_several_values_cannot_be_read_as_one() -> None:
	"""
	Check that to_value on two prices raises NotSingleValueError.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)

	with pytest.raises(ndp.NotSingleValueError):
		prices.to_value()


def test_the_numpy_copy_never_changes_the_array() -> None:
	"""
	Check that writing into to_numpy leaves the Array unchanged.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)
	numpy_prices = prices.to_numpy()

	numpy_prices[FIRST_POSITION] = CHANGED_PRICE

	price_list = prices.to_list()
	assert price_list == PRICES


def test_integers_equal_decimals_when_types_are_ignored() -> None:
	"""
	Check that [1, 2] equals [1.0, 2.0] by default.

	.. versionadded:: 0.1.0
	"""
	integers = ndp.Array.from_list(INTEGERS)
	decimals = ndp.Array.from_list(DECIMALS)

	equality = ndp.Equality(other=decimals)
	is_equal = integers.is_equal(equality)

	assert is_equal


def test_integers_differ_from_decimals_when_types_are_strict() -> None:
	"""
	Check that [1, 2] differs from [1.0, 2.0] with TypeMatch.STRICT.

	.. versionadded:: 0.1.0
	"""
	integers = ndp.Array.from_list(INTEGERS)
	decimals = ndp.Array.from_list(DECIMALS)
	equality = ndp.Equality(other=decimals, types=ndp.TypeMatch.STRICT)

	is_equal = integers.is_equal(equality)

	assert not is_equal


def test_missing_values_at_the_same_place_are_equal() -> None:
	"""
	Check that two Arrays with a missing value at the same position are equal.

	.. versionadded:: 0.1.0
	"""
	temperatures = ndp.Array.from_list(TEMPERATURES)
	same_temperatures = ndp.Array.from_list(TEMPERATURES)

	equality = ndp.Equality(other=same_temperatures)
	is_equal = temperatures.is_equal(equality)

	assert is_equal


def test_an_array_shows_its_values_and_type() -> None:
	"""
	Check the text of an Array.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)

	prices_text = repr(prices)

	assert prices_text == EXPECTED_PRICES_TEXT


def test_an_array_holding_complex_numbers_is_rejected() -> None:
	"""
	Check that numpy complex numbers raise UnsupportedTypeError.

	.. versionadded:: 0.1.0
	"""
	complex_values = numpy.array(COMPLEX_VALUES)

	with pytest.raises(ndp.UnsupportedTypeError):
		ndp.Array.from_numpy(complex_values)

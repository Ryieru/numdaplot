"""
Functional tests of the math functions applied to an Array.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

import numdaplot as ndp

SQUARES = [1, 4, 9]
EXPECTED_ROOTS = [1.0, 2.0, 3.0]
POWERS_OF_TEN = [1, 100, 1000]
EXPECTED_DECIMAL_LOGARITHMS = [0.0, 2.0, 3.0]
HALVES = [0.5, 1.5, 2.5]
EXPECTED_ROUNDED_HALVES = [0.0, 2.0, 2.0]
PRICES = [12.346, 6.784]
EXPECTED_ROUNDED_PRICES = [12.35, 6.78]
NEGATIVE_VALUES = [4, -9]
TEMPERATURES = [16.0, None]
EXPECTED_MISSING_MASK = [False, True]
DECIMAL_BASE = 10
CENT_DECIMALS = 2
TEXTS = ["a"]


def test_square_roots_are_computed() -> None:
	"""
	Check the square roots of 1, 4 and 9.

	.. versionadded:: 0.1.0
	"""
	squares = ndp.Array.from_list(SQUARES)

	roots = squares.apply(ndp.SquareRoot())

	root_list = roots.to_list()
	assert root_list == EXPECTED_ROOTS


def test_decimal_logarithms_are_exact_on_powers_of_ten() -> None:
	"""
	Check that the logarithm in base 10 of 1000 is exactly 3.

	.. versionadded:: 0.1.0
	"""
	powers = ndp.Array.from_list(POWERS_OF_TEN)

	logarithms = powers.apply(ndp.Logarithm(base=DECIMAL_BASE))

	logarithm_list = logarithms.to_list()
	assert logarithm_list == EXPECTED_DECIMAL_LOGARITHMS


def test_halves_are_rounded_to_the_nearest_even_number() -> None:
	"""
	Check that 0.5, 1.5 and 2.5 give 0, 2 and 2 with the default decimals, as in numpy.

	.. versionadded:: 0.1.0
	"""
	halves = ndp.Array.from_list(HALVES)

	rounded_halves = halves.apply(ndp.Round())

	rounded_list = rounded_halves.to_list()
	assert rounded_list == EXPECTED_ROUNDED_HALVES


def test_prices_are_rounded_to_cents() -> None:
	"""
	Check that two decimals are kept.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)

	rounded_prices = prices.apply(ndp.Round(decimals=CENT_DECIMALS))

	rounded_list = rounded_prices.to_list()
	is_close = numpy.allclose(rounded_list, EXPECTED_ROUNDED_PRICES)
	assert is_close


def test_the_square_root_of_a_negative_value_is_rejected() -> None:
	"""
	Check that -9 raises OutOfDomainError.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list(NEGATIVE_VALUES)

	with pytest.raises(ndp.OutOfDomainError):
		values.apply(ndp.SquareRoot())


def test_missing_values_stay_missing() -> None:
	"""
	Check that a missing temperature stays missing after a math function.

	.. versionadded:: 0.1.0
	"""
	temperatures = ndp.Array.from_list(TEMPERATURES)

	roots = temperatures.apply(ndp.SquareRoot())

	missing_mask = roots.check(ndp.IsMissing())
	missing_list = missing_mask.to_list()
	assert missing_list == EXPECTED_MISSING_MASK


def test_a_math_function_on_texts_is_rejected() -> None:
	"""
	Check that Absolute on texts raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	texts = ndp.Array.from_list(TEXTS)

	with pytest.raises(ndp.IncompatibleTypesError):
		texts.apply(ndp.Absolute())


def test_square_roots_of_small_integers_are_decimals_of_64_bits() -> None:
	"""
	Check that the square roots of INT8 values are FLOAT64 values.

	.. versionadded:: 0.2.0
	"""
	squares = ndp.Array.from_list(SQUARES, dtype=ndp.Type.INT8)

	roots = squares.apply(ndp.SquareRoot())

	root_values = roots.to_list()
	assert roots.dtype == ndp.Type.FLOAT64
	assert root_values == EXPECTED_ROOTS

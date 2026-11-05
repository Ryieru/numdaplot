"""
Functional tests of the operators of an Array, as a user combines Arrays.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

import numdaplot as ndp

PRICES = [10.0, 20.0]
TAX_RATE = 1.2
EXPECTED_TAXED_PRICES = [12.0, 24.0]
QUANTITIES = [2, 3]
EXPECTED_TOTALS = [20.0, 60.0]
INTEGERS = [7, 8]
DIVISOR = 2
EXPECTED_HALVES = [3.5, 4.0]
GRID = [[1, 2], [3, 4]]
ROW = [10, 20]
EXPECTED_STRETCHED = [[11, 22], [13, 24]]
THREE_VALUES = [1, 2, 3]
AGES = [15, 30, 70]
ADULT_AGE = 18
RETIREMENT_AGE = 65
EXPECTED_WORKING_AGE = [False, True, False]
EURO_TEXT = "euros"


def test_an_array_is_multiplied_by_a_single_value() -> None:
	"""
	Check that each price is multiplied by the tax rate.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)

	taxed_prices = prices * TAX_RATE

	taxed_list = taxed_prices.to_list()
	is_close = numpy.allclose(taxed_list, EXPECTED_TAXED_PRICES)
	assert is_close


def test_two_arrays_are_multiplied_value_by_value() -> None:
	"""
	Check that prices times quantities give totals.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)
	quantities = ndp.Array.from_list(QUANTITIES)

	totals = prices * quantities

	total_list = totals.to_list()
	assert total_list == EXPECTED_TOTALS


def test_dividing_integers_gives_decimals() -> None:
	"""
	Check that / follows the numpy rule and gives FLOAT64.

	.. versionadded:: 0.1.0
	"""
	integers = ndp.Array.from_list(INTEGERS)

	halves = integers / DIVISOR

	half_list = halves.to_list()
	assert halves.dtype == ndp.Type.FLOAT64
	assert half_list == EXPECTED_HALVES


def test_a_row_added_to_a_grid_is_stretched_with_a_warning() -> None:
	"""
	Check that broadcasting works and emits a BroadcastWarning.

	.. versionadded:: 0.1.0
	"""
	grid = ndp.Array.from_list(GRID)
	row = ndp.Array.from_list(ROW)

	with pytest.warns(ndp.BroadcastWarning):
		stretched = grid + row

	stretched_rows = stretched.to_list()
	assert stretched_rows == EXPECTED_STRETCHED


def test_arrays_of_incompatible_shapes_are_rejected() -> None:
	"""
	Check that three values cannot be added to two.

	.. versionadded:: 0.1.0
	"""
	three_values = ndp.Array.from_list(THREE_VALUES)
	two_values = ndp.Array.from_list(QUANTITIES)

	with pytest.raises(ndp.ShapeMismatchError):
		_ = three_values + two_values


def test_a_number_cannot_be_added_to_a_text() -> None:
	"""
	Check that adding a text to numbers raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)

	with pytest.raises(ndp.IncompatibleTypesError):
		_ = prices + EURO_TEXT


def test_a_numpy_array_cannot_be_combined_with_an_array() -> None:
	"""
	Check that a raw numpy array is refused on either side.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)
	numpy_quantities = numpy.array(QUANTITIES)

	with pytest.raises(ndp.InvalidTypeError):
		_ = numpy_quantities * prices


def test_masks_are_combined_with_boolean_operators() -> None:
	"""
	Check that two checks combined with & give the working ages.

	.. versionadded:: 0.1.0
	"""
	ages = ndp.Array.from_list(AGES)
	adults = ages.check(ndp.GreaterOrEqual(ADULT_AGE))
	retired = ages.check(ndp.GreaterOrEqual(RETIREMENT_AGE))

	working_age = adults & ~retired

	working_age_list = working_age.to_list()
	assert working_age_list == EXPECTED_WORKING_AGE

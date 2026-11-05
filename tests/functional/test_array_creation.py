"""
Functional tests of the creation of an Array, as a user creates it from ndp.

.. versionadded:: 0.1.0
"""

from datetime import date

import numpy
import pytest

import numdaplot as ndp

PRICES = [12, 8, 30]
PRICES_SHAPE = ndp.Shape([3])
GRID = [[1.5, None], [3.0, 4.0]]
GRID_SHAPE = ndp.Shape([2, 2])
DATES = [date(2026, 1, 31), None]
MIXED_VALUES = [1, "a"]
AGES = [8, 30, 255]
NEGATIVE_AGES = [8, -1]
SEED = 7
DIE_SHAPE = ndp.Shape([100])
DIE_FACES = {1, 2, 3, 4, 5, 6}
EXPECTED_RANGE = [0.0, 0.25, 0.5, 0.75, 1.0]
EXPECTED_EXCLUDED_SPACING = [0.2, 0.4, 0.6, 0.8]
FILLED_SHAPE = ndp.Shape([2, 3])
EXPECTED_FILLED = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
NUMPY_TEXTS = numpy.array(["Paris", "Lyon"])


def test_a_list_of_integers_gives_an_int64_array() -> None:
	"""
	Check that integers are stored as INT64 with their shape.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)

	assert prices.dtype == ndp.Type.INT64
	assert prices.shape == PRICES_SHAPE


def test_nested_lists_with_a_missing_value_give_a_decimal_grid() -> None:
	"""
	Check that None in nested decimals gives a two-dimensional FLOAT64 Array.

	.. versionadded:: 0.1.0
	"""
	grid = ndp.Array.from_list(GRID)

	assert grid.dtype == ndp.Type.FLOAT64
	assert grid.shape == GRID_SHAPE


def test_dates_with_a_missing_date_give_a_date_array() -> None:
	"""
	Check that Python dates with None give a DATE Array, None coming back as None.

	.. versionadded:: 0.1.0
	"""
	days = ndp.Array.from_list(DATES)

	day_list = days.to_list()
	assert days.dtype == ndp.Type.DATE
	assert day_list == DATES


def test_a_list_of_integers_gives_an_unsigned_array_when_asked() -> None:
	"""
	Check that integers from 0 to 255 are stored as UINT8, and a negative one is refused.

	.. versionadded:: 0.1.0
	"""
	ages = ndp.Array.from_list(AGES, dtype=ndp.Type.UINT8)

	age_list = ages.to_list()
	assert ages.dtype == ndp.Type.UINT8
	assert age_list == AGES
	with pytest.raises(ndp.ValueConversionError):
		ndp.Array.from_list(NEGATIVE_AGES, dtype=ndp.Type.UINT8)


def test_mixed_numbers_and_texts_are_rejected() -> None:
	"""
	Check that a user mixing numbers and texts gets IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.IncompatibleTypesError):
		ndp.Array.from_list(MIXED_VALUES)


def test_a_filled_array_repeats_one_value_in_a_shape() -> None:
	"""
	Check that filled gives a grid of decimal zeros.

	.. versionadded:: 0.1.0
	"""
	zeros = ndp.Array.filled(shape=FILLED_SHAPE, value=0, dtype=ndp.Type.FLOAT64)

	zero_rows = zeros.to_list()
	assert zero_rows == EXPECTED_FILLED


def test_a_range_includes_its_stop() -> None:
	"""
	Check that a decimal range from 0 to 1 ends on 1.

	.. versionadded:: 0.1.0
	"""
	sequence = ndp.Range(start=0, stop=1, step=0.25)
	quarters = ndp.Array.from_range(sequence)

	quarter_list = quarters.to_list()
	assert quarter_list == EXPECTED_RANGE


def test_a_spacing_can_exclude_both_bounds() -> None:
	"""
	Check that four values strictly between 0 and 1 are evenly spaced.

	.. versionadded:: 0.1.0
	"""
	spacing = ndp.Spacing(start=0, stop=1, count=4, bounds=ndp.Bounds.EXCLUDED)

	inner_values = ndp.Array.from_spacing(spacing)

	inner_list = inner_values.to_list()
	is_close = numpy.allclose(inner_list, EXPECTED_EXCLUDED_SPACING)
	assert is_close


def test_a_seeded_die_is_reproducible_and_draws_every_face() -> None:
	"""
	Check that two seeded draws are equal and cover the six faces.

	.. versionadded:: 0.1.0
	"""
	die = ndp.RandomIntegers(low=1, high=6)

	first_rolls = ndp.Array.random(die, shape=DIE_SHAPE, seed=SEED)
	second_rolls = ndp.Array.random(die, shape=DIE_SHAPE, seed=SEED)

	equality = ndp.Equality(other=second_rolls)
	are_same = first_rolls.is_equal(equality)
	roll_list = first_rolls.to_list()
	faces = set(roll_list)
	assert are_same
	assert faces == DIE_FACES


def test_a_numpy_array_of_fixed_length_texts_gives_a_text_array() -> None:
	"""
	Check that numpy fixed-length texts become TEXT.

	.. versionadded:: 0.1.0
	"""
	cities = ndp.Array.from_numpy(NUMPY_TEXTS)

	assert cities.dtype == ndp.Type.TEXT

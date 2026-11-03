"""
Functional tests of the selection of Array values, by rule and by position.

.. versionadded:: 0.1.0
"""

from datetime import date

import pytest

import numdaplot as ndp

PRICES = [[5, 12], [30, 8]]
PRICE_LIMIT = 10
EXPECTED_HIGH_PRICES = [12, 30]
EXPECTED_HIGH_PRICE_MASK = [[False, True], [True, False]]
TEMPERATURES = [12.0, None, 18.0]
EXPECTED_MISSING_MASK = [False, True, False]
CITIES = ["Paris", "Lyon", "PARIS"]
SEARCHED_CITY = "paris"
EXPECTED_PARIS = ["Paris", "PARIS"]
DAYS = [date(2026, 1, 1), date(2026, 2, 1), None]
WINTER = ndp.Between(low=date(2026, 1, 15), high=date(2026, 3, 1))
EXPECTED_WINTER_DAYS = [date(2026, 2, 1)]
GRID = [[1, 2, 3], [4, 5, 6]]
LAST_ROW_FIRST_COLUMNS = ndp.Region(rows=ndp.Index(-1), columns=ndp.Range(start=0, stop=1))
EXPECTED_TAKEN = [[4, 5]]
SCORES = [10, 20, 30]
SECOND_SCORE = ndp.Region(rows=ndp.Index(1))
REPLACED_SCORE = 0
EXPECTED_REPLACED_SCORES = [10, 0, 30]
DECIMAL_SCORE = 0.5
OUTSIDE_SCORE = ndp.Region(rows=ndp.Index(3))


def test_values_above_a_limit_are_selected_in_one_dimension() -> None:
	"""
	Check that select keeps the prices above 10, in reading order.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)

	high_prices = prices.select(ndp.Greater(PRICE_LIMIT))

	high_price_list = high_prices.to_list()
	assert high_price_list == EXPECTED_HIGH_PRICES


def test_a_check_keeps_the_shape() -> None:
	"""
	Check that check gives a BOOL grid of the same shape.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)

	high_price_mask = prices.check(ndp.Greater(PRICE_LIMIT))

	mask_rows = high_price_mask.to_list()
	assert high_price_mask.dtype == ndp.Type.BOOL
	assert mask_rows == EXPECTED_HIGH_PRICE_MASK


def test_missing_values_are_found() -> None:
	"""
	Check that IsMissing finds the missing temperature.

	.. versionadded:: 0.1.0
	"""
	temperatures = ndp.Array.from_list(TEMPERATURES)

	missing_mask = temperatures.check(ndp.IsMissing())

	missing_list = missing_mask.to_list()
	assert missing_list == EXPECTED_MISSING_MASK


def test_texts_containing_a_word_are_selected_whatever_the_case() -> None:
	"""
	Check that Contains with ignored case finds every spelling of Paris.

	.. versionadded:: 0.1.0
	"""
	cities = ndp.Array.from_list(CITIES)
	rule = ndp.Contains(SEARCHED_CITY, case=ndp.Case.IGNORED)

	paris_cities = cities.select(rule)

	paris_list = paris_cities.to_list()
	assert paris_list == EXPECTED_PARIS


def test_dates_inside_a_period_are_selected_despite_a_missing_date() -> None:
	"""
	Check that a date interval works on dates holding a missing date.

	.. versionadded:: 0.1.0
	"""
	days = ndp.Array.from_list(DAYS)

	winter_days = days.select(WINTER)

	winter_list = winter_days.to_list()
	assert winter_list == EXPECTED_WINTER_DAYS


def test_a_block_of_a_grid_is_taken_by_position() -> None:
	"""
	Check that the start of the last row is taken, keeping two dimensions.

	.. versionadded:: 0.1.0
	"""
	grid = ndp.Array.from_list(GRID)

	block = grid.take(LAST_ROW_FIRST_COLUMNS)

	block_rows = block.to_list()
	assert block_rows == EXPECTED_TAKEN


def test_a_replacement_returns_a_new_array() -> None:
	"""
	Check that replace gives a new Array and leaves the original unchanged.

	.. versionadded:: 0.1.0
	"""
	scores = ndp.Array.from_list(SCORES)
	replacement = ndp.Replacement(region=SECOND_SCORE, value=REPLACED_SCORE)

	replaced_scores = scores.replace(replacement)

	replaced_list = replaced_scores.to_list()
	score_list = scores.to_list()
	assert replaced_list == EXPECTED_REPLACED_SCORES
	assert score_list == SCORES


def test_a_decimal_cannot_replace_an_integer() -> None:
	"""
	Check that a decimal written into integers raises ValueConversionError.

	.. versionadded:: 0.1.0
	"""
	scores = ndp.Array.from_list(SCORES)
	replacement = ndp.Replacement(region=SECOND_SCORE, value=DECIMAL_SCORE)

	with pytest.raises(ndp.ValueConversionError):
		scores.replace(replacement)


def test_a_position_outside_the_array_is_rejected() -> None:
	"""
	Check that position 3 of three values raises InvalidPositionError.

	.. versionadded:: 0.1.0
	"""
	scores = ndp.Array.from_list(SCORES)

	with pytest.raises(ndp.InvalidPositionError):
		scores.take(OUTSIDE_SCORE)

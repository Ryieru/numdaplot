"""
Functional tests of the Python operations an Array refuses, as a user tries them.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp

PRICES = [10, 20]
LIMIT = 15
EXPECTED_LESS_MESSAGE = "use select or check with a rule such as ndp.Less"
EXPECTED_LOOP_VALUES = [10, 20]


def test_comparing_with_less_than_points_to_select_and_check() -> None:
	"""
	Check that < is refused with a message naming ndp.Less.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)

	with pytest.raises(ndp.RefusedOperationError, match=EXPECTED_LESS_MESSAGE):
		_ = prices < LIMIT


def test_brackets_are_refused() -> None:
	"""
	Check that reading by brackets is refused.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)

	with pytest.raises(ndp.RefusedOperationError):
		_ = prices[0]


def test_equality_with_double_equal_is_refused() -> None:
	"""
	Check that == is refused, is_equal being the way to compare.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)
	same_prices = ndp.Array.from_list(PRICES)

	with pytest.raises(ndp.RefusedOperationError):
		_ = prices == same_prices


def test_a_loop_goes_through_to_list() -> None:
	"""
	Check that looping directly is refused while looping over to_list works.

	.. versionadded:: 0.1.0
	"""
	prices = ndp.Array.from_list(PRICES)
	looped_values = list[object]()

	with pytest.raises(ndp.RefusedOperationError):
		iter(prices)

	price_list = prices.to_list()
	for price in price_list:
		looped_values.append(price)

	assert looped_values == EXPECTED_LOOP_VALUES

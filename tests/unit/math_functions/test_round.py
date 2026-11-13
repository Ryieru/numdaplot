"""
Unit tests of Round.

.. versionadded:: 0.1.0
"""

from numdaplot.math_functions.round import Round

CENT_DECIMALS = 2


def test_round_keeps_no_decimal_by_default() -> None:
	"""
	Check that the values are rounded to whole numbers by default.

	.. versionadded:: 0.1.0
	"""
	rounding = Round()

	assert rounding.decimals == 0


def test_round_keeps_its_decimals() -> None:
	"""
	Check that given decimals are available as an attribute.

	.. versionadded:: 0.1.0
	"""
	rounding = Round(decimals=CENT_DECIMALS)

	assert rounding.decimals == CENT_DECIMALS

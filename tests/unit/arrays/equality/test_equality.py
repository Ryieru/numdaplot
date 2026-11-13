"""
Unit tests of Equality.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array import Array
from numdaplot.arrays.equality.equality import Equality
from numdaplot.arrays.equality.type_match import TypeMatch

COMPARED_VALUES = [1, 2]


def test_equality_ignores_types_by_default() -> None:
	"""
	Check that only the values are compared by default.

	.. versionadded:: 0.1.0
	"""
	other = Array.from_list(COMPARED_VALUES)

	equality = Equality(other=other)

	assert equality.types == TypeMatch.IGNORED


def test_equality_keeps_the_compared_array() -> None:
	"""
	Check that the compared Array is kept as given.

	.. versionadded:: 0.1.0
	"""
	other = Array.from_list(COMPARED_VALUES)

	equality = Equality(other=other, types=TypeMatch.STRICT)

	assert equality.other is other


def test_equality_compares_settings_by_identity() -> None:
	"""
	Check that two settings are compared without comparing their Arrays, which Array refuses.

	.. versionadded:: 0.1.0
	"""
	other = Array.from_list(COMPARED_VALUES)
	first_equality = Equality(other=other)
	second_equality = Equality(other=other)

	assert first_equality != second_equality

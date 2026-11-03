"""
Unit tests of are_equal.

.. versionadded:: 0.1.0
"""

import numpy

from numdaplot.arrays.conversion.equality_check import are_equal
from numdaplot.arrays.type_match import TypeMatch

INTEGERS = [1, 2]
DECIMALS = [1.0, 2.0]
OTHER_INTEGERS = [1, 3]
DECIMALS_WITH_MISSING = [1.0, numpy.nan]
TEXT_DTYPE = "T"
TEXTS = ["1", "2"]
GRID = [[1, 2]]


def test_are_equal_ignores_types_when_asked() -> None:
	"""
	Check that integers equal the same decimals with TypeMatch.IGNORED.

	.. versionadded:: 0.1.0
	"""
	integers = numpy.array(INTEGERS)
	decimals = numpy.array(DECIMALS)

	is_equal = are_equal(integers, decimals, TypeMatch.IGNORED)

	assert is_equal


def test_are_equal_compares_types_when_strict() -> None:
	"""
	Check that integers differ from the same decimals with TypeMatch.STRICT.

	.. versionadded:: 0.1.0
	"""
	integers = numpy.array(INTEGERS)
	decimals = numpy.array(DECIMALS)

	is_equal = are_equal(integers, decimals, TypeMatch.STRICT)

	assert not is_equal


def test_are_equal_detects_a_different_value() -> None:
	"""
	Check that one different value is enough.

	.. versionadded:: 0.1.0
	"""
	integers = numpy.array(INTEGERS)
	other_integers = numpy.array(OTHER_INTEGERS)

	is_equal = are_equal(integers, other_integers, TypeMatch.IGNORED)

	assert not is_equal


def test_are_equal_treats_two_missing_values_as_equal() -> None:
	"""
	Check that NaN at the same position counts as equal.

	.. versionadded:: 0.1.0
	"""
	left = numpy.array(DECIMALS_WITH_MISSING)
	right = numpy.array(DECIMALS_WITH_MISSING)

	is_equal = are_equal(left, right, TypeMatch.IGNORED)

	assert is_equal


def test_are_equal_never_matches_two_families() -> None:
	"""
	Check that numbers never equal texts.

	.. versionadded:: 0.1.0
	"""
	integers = numpy.array(INTEGERS)
	texts = numpy.array(TEXTS, dtype=TEXT_DTYPE)

	is_equal = are_equal(integers, texts, TypeMatch.IGNORED)

	assert not is_equal


def test_are_equal_detects_different_shapes() -> None:
	"""
	Check that the same values in another shape are not equal.

	.. versionadded:: 0.1.0
	"""
	integers = numpy.array(INTEGERS)
	grid = numpy.array(GRID)

	is_equal = are_equal(integers, grid, TypeMatch.IGNORED)

	assert not is_equal

"""
Unit tests of find_missing.

.. versionadded:: 0.1.0
"""

import numpy

from numdaplot.arrays.selection.missing_mask import find_missing
from numdaplot.data_types.numpy_mapping import to_numpy_dtype
from numdaplot.data_types.type import Type

DECIMALS = [1.0, numpy.nan]
DATES = numpy.array(["2026-01-31", "NaT"], dtype="datetime64[D]")
DURATIONS = numpy.array([1, "NaT"], dtype="timedelta64[s]")
INTEGERS = [[1, 2], [3, 4]]
EXPECTED_MASK = [False, True]
NO_MISSING_GRID = [[False, False], [False, False]]


def test_find_missing_finds_nan_among_decimals() -> None:
	"""
	Check that NaN is missing.

	.. versionadded:: 0.1.0
	"""
	decimals = numpy.array(DECIMALS)

	missing = find_missing(decimals)

	missing_list = missing.tolist()
	assert missing_list == EXPECTED_MASK


def test_find_missing_finds_nat_among_dates() -> None:
	"""
	Check that NaT is missing in a date array.

	.. versionadded:: 0.1.0
	"""
	missing = find_missing(DATES)

	missing_list = missing.tolist()
	assert missing_list == EXPECTED_MASK


def test_find_missing_finds_nat_among_durations() -> None:
	"""
	Check that NaT is missing in a duration array.

	.. versionadded:: 0.1.0
	"""
	missing = find_missing(DURATIONS)

	missing_list = missing.tolist()
	assert missing_list == EXPECTED_MASK


def test_find_missing_finds_nan_among_texts() -> None:
	"""
	Check that NaN is the missing value of texts, and that the text nan is present.

	.. versionadded:: 0.1.0
	"""
	text_dtype = to_numpy_dtype(Type.TEXT)
	texts = numpy.array(["nan", numpy.nan], dtype=text_dtype)

	missing = find_missing(texts)

	assert missing.tolist() == [False, True]


def test_find_missing_finds_nothing_among_integers_and_keeps_the_shape() -> None:
	"""
	Check that integers are never missing, in a mask of the same shape.

	.. versionadded:: 0.1.0
	"""
	integers = numpy.array(INTEGERS)

	missing = find_missing(integers)

	missing_rows = missing.tolist()
	assert missing_rows == NO_MISSING_GRID

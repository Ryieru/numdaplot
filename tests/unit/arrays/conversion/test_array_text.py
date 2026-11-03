"""
Unit tests of format_array.

.. versionadded:: 0.1.0
"""

import numpy

from numdaplot.arrays.conversion.array_text import format_array

LINE = [1, 2, 3]
EXPECTED_LINE_TEXT = "Array([1, 2, 3], dtype=INT64)"
GRID = [[1, 2], [3, 4]]
EXPECTED_GRID_TEXT = "Array([[1, 2],\n       [3, 4]], dtype=INT64)"
LONG_RANGE_SIZE = 2001
SHORTENING_MARK = "..."


def test_format_array_shows_values_and_type() -> None:
	"""
	Check the text of a one-dimensional Array.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(LINE)

	array_text = format_array(values)

	assert array_text == EXPECTED_LINE_TEXT


def test_format_array_aligns_rows_under_the_prefix() -> None:
	"""
	Check that the second row is aligned under the first one.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)

	array_text = format_array(values)

	assert array_text == EXPECTED_GRID_TEXT


def test_format_array_shortens_long_arrays() -> None:
	"""
	Check that a long Array is shortened with an ellipsis.

	.. versionadded:: 0.1.0
	"""
	values = numpy.arange(LONG_RANGE_SIZE)

	array_text = format_array(values)

	assert SHORTENING_MARK in array_text

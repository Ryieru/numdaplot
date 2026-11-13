"""
Unit tests of format_array.

.. versionadded:: 0.1.0
"""

import numpy

from numdaplot.arrays.export.array_text import format_array

LINE = [1, 2, 3]
EXPECTED_LINE_TEXT = "Array([1, 2, 3], dtype=INT64)"
GRID = [[1, 2], [3, 4]]
EXPECTED_GRID_TEXT = "Array([[1, 2],\n       [3, 4]], dtype=INT64)"
LONG_RANGE_SIZE = 2001
SHORTENING_MARK = "..."
DATETIMES = numpy.array(["2026-01-02T10:30", "NaT"], dtype="datetime64[ns]")
DURATIONS = numpy.array([36], dtype="timedelta64[h]")
EXPECTED_DATETIME_TEXT = "Array(['2026-01-02 10:30:00', 'NaT'], dtype=DATETIME)"
EXPECTED_DURATION_TEXT = "Array(['1 days 12:00:00'], dtype=DURATION)"
STORED_TIMES = numpy.array([56100000000, "NaT"], dtype="timedelta64[us]")
EXPECTED_TIME_TEXT = "Array(['15:35:00', 'NaT'], dtype=TIME)"


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


def test_format_array_writes_datetimes_without_t_nor_nanoseconds() -> None:
	"""
	Check the text of a datetime Array.

	.. versionadded:: 0.1.0
	"""
	array_text = format_array(DATETIMES)

	assert array_text == EXPECTED_DATETIME_TEXT


def test_format_array_writes_durations_as_pandas_writes_them() -> None:
	"""
	Check the text of a duration Array.

	.. versionadded:: 0.1.0
	"""
	array_text = format_array(DURATIONS)

	assert array_text == EXPECTED_DURATION_TEXT


def test_format_array_writes_times_of_day() -> None:
	"""
	Check the text of an Array of times.

	.. versionadded:: 0.1.0
	"""
	array_text = format_array(STORED_TIMES)

	assert array_text == EXPECTED_TIME_TEXT

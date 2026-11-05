"""
Unit tests of to_python_list.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime, timedelta

import numpy

from numdaplot.arrays.conversion.python_values import to_python_list
from numdaplot.data_types.numpy_mapping import to_numpy_dtype
from numdaplot.data_types.type import Type

DATETIMES = numpy.array(["2026-01-31T08:30", "NaT"], dtype="datetime64[ns]")
EXPECTED_DATETIMES = [datetime(2026, 1, 31, 8, 30), None]
DATES = numpy.array(["2026-01-31"], dtype="datetime64[D]")
EXPECTED_DATES = [date(2026, 1, 31)]
DURATIONS = numpy.array([3600], dtype="timedelta64[s]")
EXPECTED_DURATIONS = [timedelta(hours=1)]
GRID = [[1, 2], [3, 4]]


def test_to_python_list_gives_none_for_missing_texts() -> None:
	"""
	Check that a missing text becomes None, at any depth.

	.. versionadded:: 0.1.0
	"""
	text_dtype = to_numpy_dtype(Type.TEXT)
	texts = numpy.array([["a", numpy.nan], ["b", "c"]], dtype=text_dtype)

	python_values = to_python_list(texts)

	assert python_values == [["a", None], ["b", "c"]]


def test_to_python_list_converts_datetimes_and_missing_datetimes() -> None:
	"""
	Check that nanosecond datetimes become datetime objects and NaT becomes None.

	.. versionadded:: 0.1.0
	"""
	python_values = to_python_list(DATETIMES)

	assert python_values == EXPECTED_DATETIMES


def test_to_python_list_converts_dates() -> None:
	"""
	Check that day dates become date objects.

	.. versionadded:: 0.1.0
	"""
	python_values = to_python_list(DATES)

	assert python_values == EXPECTED_DATES


def test_to_python_list_converts_durations() -> None:
	"""
	Check that durations become timedelta objects.

	.. versionadded:: 0.1.0
	"""
	python_values = to_python_list(DURATIONS)

	assert python_values == EXPECTED_DURATIONS


def test_to_python_list_nests_one_list_per_row() -> None:
	"""
	Check that a grid gives a list of rows.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)

	python_values = to_python_list(values)

	assert python_values == GRID

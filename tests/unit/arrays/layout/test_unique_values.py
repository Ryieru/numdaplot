"""
Unit tests of find_unique_values.

.. versionadded:: 0.1.0
"""

import numpy

from numdaplot.arrays.layout.unique_values import find_unique_values

GRID = [[3, 1], [1, 3]]
EXPECTED_UNIQUE_INTEGERS = [1, 3]
DATES = numpy.array(["2026-01-02", "NaT", "2026-01-01", "NaT"], dtype="datetime64[D]")
EXPECTED_UNIQUE_DATE_COUNT = 3
LAST_POSITION = -1


def test_find_unique_values_sorts_distinct_values_in_one_dimension() -> None:
	"""
	Check that a grid gives each distinct value once, sorted, in one dimension.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)

	unique_values = find_unique_values(values)

	unique_list = unique_values.tolist()
	assert unique_list == EXPECTED_UNIQUE_INTEGERS


def test_find_unique_values_keeps_a_single_missing_value_last() -> None:
	"""
	Check that two NaT give a single NaT at the end.

	.. versionadded:: 0.1.0
	"""
	unique_values = find_unique_values(DATES)

	last_value = unique_values[LAST_POSITION]
	is_missing_last = numpy.isnat(last_value)
	assert unique_values.size == EXPECTED_UNIQUE_DATE_COUNT
	assert is_missing_last

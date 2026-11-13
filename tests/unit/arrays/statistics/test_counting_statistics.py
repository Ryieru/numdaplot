"""
Unit tests of the statistics counting values.

.. versionadded:: 0.1.0
"""

import numpy

from numdaplot.arrays.statistics.counting_statistics import (
	apply_to_each_slice,
	compute_count,
	compute_count_distinct,
	compute_most_frequent,
	compute_most_frequent_count,
	count_distinct_values,
	count_most_frequent_value,
	find_most_frequent_value,
	find_present_values,
)
from numdaplot.statistics.count import Count
from numdaplot.statistics.count_distinct import CountDistinct
from numdaplot.statistics.counted_missing import CountedMissing
from numdaplot.statistics.most_frequent import MostFrequent
from numdaplot.statistics.most_frequent_count import MostFrequentCount

DECIMALS = [2.0, numpy.nan, 2.0, 5.0]
PRESENT_COUNT = 3
ROWS_WITH_MISSING = [[1.0, numpy.nan], [numpy.nan, numpy.nan]]
LAST_AXIS = -1
EXPECTED_EVERY_VALUE_COUNTS = [2, 2]
DISTINCT_COUNT = 2
MOST_FREQUENT_VALUE = 2.0
MOST_FREQUENT_COUNT = 2
PRESENT_DECIMALS = [2.0, 2.0, 5.0]
TIED_VALUES = [2, 1, 2, 1]
LOWEST_TIED_VALUE = 1
MISSING_ONLY = [numpy.nan]
NO_VALUE_COUNT = 0
TEXT_ROWS = numpy.array([["a", "b", "b"], ["c", "c", "a"]], dtype="T")
ROW_AXIS = 1
EXPECTED_ROW_MOST_FREQUENT = ["b", "c"]
GRID = [[1, 1], [1, 2]]
EXPECTED_ROW_DISTINCT_COUNTS = [1, 2]


def test_compute_count_counts_present_values() -> None:
	"""
	Check that NaN is not counted.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(DECIMALS)

	count = compute_count(values, None, Count())

	assert count == PRESENT_COUNT


def test_compute_count_distinct_counts_each_present_value_once() -> None:
	"""
	Check that 2.0, 2.0 and 5.0 give two distinct values.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(DECIMALS)

	distinct_count = compute_count_distinct(values, None, CountDistinct())

	assert distinct_count == DISTINCT_COUNT


def test_compute_most_frequent_finds_the_most_frequent_value() -> None:
	"""
	Check that 2.0 is the most frequent value.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(DECIMALS)

	most_frequent_value = compute_most_frequent(values, None, MostFrequent())

	assert most_frequent_value == MOST_FREQUENT_VALUE


def test_compute_most_frequent_count_counts_the_most_frequent_value() -> None:
	"""
	Check that 2.0 appears twice.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(DECIMALS)

	most_frequent_count = compute_most_frequent_count(values, None, MostFrequentCount())

	assert most_frequent_count == MOST_FREQUENT_COUNT


def test_apply_to_each_slice_gives_one_result_per_row() -> None:
	"""
	Check that an axis applies the function to each row.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)

	distinct_counts = apply_to_each_slice(values, ROW_AXIS, count_distinct_values)

	distinct_count_list = distinct_counts.tolist()
	assert distinct_count_list == EXPECTED_ROW_DISTINCT_COUNTS


def test_apply_to_each_slice_handles_texts() -> None:
	"""
	Check the most frequent text of each row.

	.. versionadded:: 0.1.0
	"""
	most_frequent_texts = apply_to_each_slice(TEXT_ROWS, ROW_AXIS, find_most_frequent_value)

	most_frequent_list = most_frequent_texts.tolist()
	assert most_frequent_list == EXPECTED_ROW_MOST_FREQUENT


def test_find_present_values_drops_missing_values() -> None:
	"""
	Check that NaN is dropped.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(DECIMALS)

	present_values = find_present_values(values)

	present_list = present_values.tolist()
	assert present_list == PRESENT_DECIMALS


def test_find_most_frequent_value_keeps_the_lowest_value_of_a_tie() -> None:
	"""
	Check that 1 wins a tie against 2.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(TIED_VALUES)

	most_frequent_value = find_most_frequent_value(values)

	assert most_frequent_value == LOWEST_TIED_VALUE


def test_count_most_frequent_value_gives_zero_without_present_value() -> None:
	"""
	Check that only missing values give a count of 0.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(MISSING_ONLY)

	most_frequent_count = count_most_frequent_value(values)

	assert most_frequent_count == NO_VALUE_COUNT


def test_compute_count_includes_the_missing_values_on_demand() -> None:
	"""
	Check that NaN is counted with CountedMissing.INCLUDED.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(DECIMALS)

	count = compute_count(values, None, Count(missing=CountedMissing.INCLUDED))

	assert count == values.size


def test_compute_count_includes_the_missing_values_of_each_row() -> None:
	"""
	Check that including the missing values keeps one count per reduced slice.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(ROWS_WITH_MISSING)

	counts = compute_count(values, LAST_AXIS, Count(missing=CountedMissing.INCLUDED))

	count_list = counts.tolist()
	assert count_list == EXPECTED_EVERY_VALUE_COUNTS

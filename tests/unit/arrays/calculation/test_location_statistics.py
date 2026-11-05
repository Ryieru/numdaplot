"""
Unit tests of the statistics locating or summing values.

.. versionadded:: 0.1.0
"""

from collections.abc import Callable
from typing import Any

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays.calculation.location_statistics import (
	compute_maximum,
	compute_mean,
	compute_median,
	compute_minimum,
	compute_quantile,
	compute_standard_deviation,
	compute_sum,
)
from numdaplot.data_types.numpy_mapping import to_numpy_dtype
from numdaplot.data_types.type import Type
from numdaplot.statistics.maximum import Max
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.median import Median
from numdaplot.statistics.minimum import Min
from numdaplot.statistics.quantile import Quantile
from numdaplot.statistics.standard_deviation import StandardDeviation
from numdaplot.statistics.statistic import Statistic
from numdaplot.statistics.sum import Sum

type StatisticFunction = Callable[[NDArray[Any], int | None, Statistic], Any]
DECIMALS_WITH_MISSING = [1.0, numpy.nan, 3.0, 8.0]
STATISTICS = [
	(compute_sum, Sum(), 12.0),
	(compute_mean, Mean(), 4.0),
	(compute_median, Median(), 3.0),
	(compute_minimum, Min(), 1.0),
	(compute_maximum, Max(), 8.0),
	(compute_quantile, Quantile(0.5), 3.0),
]
SPREAD_VALUES = [0, 10, 20]
EXPECTED_POPULATION_DEVIATION = 8.16496580927726
GRID = [[1, 2], [3, 4]]
COLUMN_AXIS = 0
EXPECTED_COLUMN_SUMS = [4, 6]
TEXT_DTYPE = "T"
TEXTS = ["b", "c", "a"]
FIRST_TEXT = "a"
DATES = numpy.array(["2026-03-01", "NaT", "2025-01-01"], dtype="datetime64[D]")
EARLIEST_DATE = numpy.datetime64("2025-01-01")


@pytest.mark.parametrize(("function", "statistic", "expected_result"), STATISTICS)
def test_location_statistics_ignore_missing_values(
	function: StatisticFunction, statistic: Statistic, expected_result: float
) -> None:
	"""
	Check each statistic on decimals holding a NaN.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function
		The function computing the statistic.
	statistic
		The statistic.
	expected_result
		Its result without the NaN.
	"""
	values = numpy.array(DECIMALS_WITH_MISSING)

	result = function(values, None, statistic)

	assert result == expected_result


def test_compute_standard_deviation_divides_by_the_number_of_values() -> None:
	"""
	Check the population standard deviation of 0, 10 and 20.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(SPREAD_VALUES)

	deviation = compute_standard_deviation(values, None, StandardDeviation())

	is_close = numpy.allclose(deviation, EXPECTED_POPULATION_DEVIATION)
	assert is_close


def test_compute_sum_reduces_along_an_axis() -> None:
	"""
	Check that an axis gives one sum per column.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)

	sums = compute_sum(values, COLUMN_AXIS, Sum())

	sum_list = sums.tolist()
	assert sum_list == EXPECTED_COLUMN_SUMS


def test_compute_minimum_orders_texts_alphabetically() -> None:
	"""
	Check that the minimum of texts is the first in alphabetical order.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(TEXTS, dtype=TEXT_DTYPE)

	minimum = compute_minimum(values, None, Min())

	assert minimum == FIRST_TEXT


def test_compute_minimum_ignores_missing_texts() -> None:
	"""
	Check that a missing text is not the lowest text.

	.. versionadded:: 0.1.0
	"""
	text_dtype = to_numpy_dtype(Type.TEXT)
	texts = numpy.array(["b", numpy.nan, "a"], dtype=text_dtype)

	minimum = compute_minimum(texts, None, Min())

	assert minimum == "a"


def test_compute_maximum_ignores_missing_texts() -> None:
	"""
	Check that a missing text is not the highest text.

	.. versionadded:: 0.1.0
	"""
	text_dtype = to_numpy_dtype(Type.TEXT)
	texts = numpy.array(["b", numpy.nan, "a"], dtype=text_dtype)

	maximum = compute_maximum(texts, None, Max())

	assert maximum == "b"


def test_compute_maximum_ignores_missing_texts_along_an_axis() -> None:
	"""
	Check that each slice gives its highest present text.

	.. versionadded:: 0.1.0
	"""
	text_dtype = to_numpy_dtype(Type.TEXT)
	texts = numpy.array([["a", numpy.nan], ["b", "c"]], dtype=text_dtype)

	maximums = compute_maximum(texts, 1, Max())

	assert maximums.tolist() == ["a", "c"]


def test_compute_minimum_ignores_missing_dates() -> None:
	"""
	Check that the earliest date is found despite NaT.

	.. versionadded:: 0.1.0
	"""
	minimum = compute_minimum(DATES, None, Min())

	assert minimum == EARLIEST_DATE

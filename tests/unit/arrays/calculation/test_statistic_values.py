"""
Unit tests of compute_statistic and require_present_values.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

from numdaplot.arrays.calculation.statistic_values import compute_statistic, require_present_values
from numdaplot.errors.dimension_error import DimensionError
from numdaplot.errors.empty_array_error import EmptyArrayError
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.positions.axis import Axis
from numdaplot.rules.greater import Greater
from numdaplot.statistics.counted_missing import CountedMissing
from numdaplot.statistics.maximum import Max
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.share import Share
from numdaplot.statistics.statistic import Statistic
from numdaplot.statistics.sum import Sum

DECIMALS = [1.0, numpy.nan, 3.0]
SINGLE_DIMENSION = (1,)
EXPECTED_MEAN = [2.0]
GRID = [[1, 2], [3, 4]]
EXPECTED_ROW_SUMS = [3, 7]
EXPECTED_COLUMN_SUMS = [4, 6]
TEXT_DTYPE = "T"
TEXTS = ["b", "a"]
LAST_TEXT = ["b"]
TEXT_KIND = "T"
MISSING_ROWS = [[1.0, numpy.nan], [numpy.nan, numpy.nan]]
MISSING_ONLY = [numpy.nan]
AGES = [70.0, numpy.nan, 30.0, 80.0]
SENIOR_AGE = 65
EXPECTED_PRESENT_SHARE = [2 / 3]
EXPECTED_EVERY_SHARE = [0.5]
EXPECTED_ROW_SHARES = [0.5, 0.0]


class UnknownStatistic(Statistic):
	"""
	A statistic numdaplot does not know.

	.. versionadded:: 0.1.0
	"""


def test_compute_statistic_gives_a_single_value_without_axis() -> None:
	"""
	Check that the mean of the whole Array is one value in one dimension.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(DECIMALS)

	result = compute_statistic(values, Mean(), None)

	result_list = result.tolist()
	assert result.shape == SINGLE_DIMENSION
	assert result_list == EXPECTED_MEAN


def test_compute_statistic_gives_one_value_per_row() -> None:
	"""
	Check that EACH_ROW gives the sum of each row.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)

	result = compute_statistic(values, Sum(), Axis.EACH_ROW)

	result_list = result.tolist()
	assert result_list == EXPECTED_ROW_SUMS


def test_compute_statistic_gives_one_value_per_column() -> None:
	"""
	Check that EACH_COLUMN gives the sum of each column.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)

	result = compute_statistic(values, Sum(), Axis.EACH_COLUMN)

	result_list = result.tolist()
	assert result_list == EXPECTED_COLUMN_SUMS


def test_compute_statistic_stores_a_text_result_as_variable_length_text() -> None:
	"""
	Check that the maximum of texts stays a TEXT value.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(TEXTS, dtype=TEXT_DTYPE)

	result = compute_statistic(values, Max(), None)

	result_list = result.tolist()
	assert result_list == LAST_TEXT
	assert result.dtype.kind == TEXT_KIND


def test_compute_statistic_rejects_a_statistic_not_applying_to_the_type() -> None:
	"""
	Check that the mean of texts raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(TEXTS, dtype=TEXT_DTYPE)

	with pytest.raises(IncompatibleTypesError):
		compute_statistic(values, Mean(), None)


def test_compute_statistic_rejects_an_axis_on_one_dimension() -> None:
	"""
	Check that an axis on a one-dimensional Array raises DimensionError.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(DECIMALS)

	with pytest.raises(DimensionError):
		compute_statistic(values, Sum(), Axis.EACH_ROW)


def test_compute_statistic_rejects_a_row_without_present_value() -> None:
	"""
	Check that the mean of a row of NaN raises EmptyArrayError.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(MISSING_ROWS)

	with pytest.raises(EmptyArrayError):
		compute_statistic(values, Mean(), Axis.EACH_ROW)


def test_compute_statistic_refuses_an_unknown_statistic() -> None:
	"""
	Check that a statistic outside numdaplot raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(DECIMALS)

	with pytest.raises(RefusedOperationError):
		compute_statistic(values, UnknownStatistic(), None)


def test_require_present_values_accepts_one_present_value() -> None:
	"""
	Check that a single present value is enough.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(DECIMALS)

	require_present_values(values, None, Mean.__name__)


def test_require_present_values_rejects_only_missing_values() -> None:
	"""
	Check that only NaN raises EmptyArrayError.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(MISSING_ONLY)

	with pytest.raises(EmptyArrayError):
		require_present_values(values, None, Mean.__name__)


def test_compute_statistic_divides_a_share_by_the_present_values() -> None:
	"""
	Check that a share leaves the missing values out of its total by default.

	.. versionadded:: 0.2.0
	"""
	values = numpy.array(AGES)

	shares = compute_statistic(values, Share(rule=Greater(SENIOR_AGE)), None)

	share_list = shares.tolist()
	assert share_list == EXPECTED_PRESENT_SHARE


def test_compute_statistic_divides_a_share_by_every_value_when_missing_values_count() -> None:
	"""
	Check that a share including the missing values counts them as not satisfying the rule.

	.. versionadded:: 0.2.0
	"""
	values = numpy.array(AGES)
	share = Share(rule=Greater(SENIOR_AGE), missing=CountedMissing.INCLUDED)

	shares = compute_statistic(values, share, None)

	share_list = shares.tolist()
	assert share_list == EXPECTED_EVERY_SHARE


def test_compute_statistic_gives_one_share_per_row() -> None:
	"""
	Check one share per row, missing values counted.

	.. versionadded:: 0.2.0
	"""
	values = numpy.array(MISSING_ROWS)
	share = Share(rule=Greater(0), missing=CountedMissing.INCLUDED)

	shares = compute_statistic(values, share, Axis.EACH_ROW)

	share_list = shares.tolist()
	assert share_list == EXPECTED_ROW_SHARES


def test_compute_statistic_rejects_a_share_without_present_value() -> None:
	"""
	Check that a share of missing values only raises EmptyArrayError when they are left out.

	.. versionadded:: 0.2.0
	"""
	values = numpy.array(MISSING_ONLY)

	with pytest.raises(EmptyArrayError):
		compute_statistic(values, Share(rule=Greater(SENIOR_AGE)), None)

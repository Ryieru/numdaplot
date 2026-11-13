"""
Unit tests of the count of the missing values of a Table.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

import numpy
import pandas
import pytest

from numdaplot.column_storage.column_values import find_column_type
from numdaplot.measures.measure import Measure
from numdaplot.positions.axis import Axis
from numdaplot.tables.missing.missing_count import MissingCount
from numdaplot.tables.missing.missing_counts import (
	build_name_column,
	count_axis_missing,
	count_frame_missing,
	find_frame_missing,
)
from numdaplot.types.type import Type

FRAME = pandas.DataFrame(
	{
		"city": pandas.Series(["Paris", None, "Pau", "Nice"], dtype="string"),
		"price": [120.0, None, None, 90.0],
	}
)
EMPTY_FRAME = pandas.DataFrame({"price": pandas.Series(dtype="float64")})
EXPECTED_MISSING_GRID = [[False, False], [True, True], [False, True], [False, False]]
EXPECTED_NAMES = ["city", "price"]
COUNT_NAME = "missing_count"
RATIO_NAME = "missing_ratio"
NAMES_COLUMN = "column"
MISSING_GRID = numpy.array([[True, False], [True, True], [False, False]])
EXPECTED_ROW_COUNTS = [1, 2, 0]
EXPECTED_COLUMN_COUNTS = [2, 1]
EXPECTED_TOTAL_COUNTS = [3]
COLUMN_COUNT = 2
ROW_COUNT = 3
CELL_COUNT = 6


@dataclass(frozen=True)
class CountCase:
	"""
	A count of the missing values of FRAME and its expected result.

	.. versionadded:: 0.1.0

	Parameters
	----------
	missing_count
		The settings of the count.
	axis
		The axis of the count, or None for the whole Table.
	expected_column_names
		The names of the columns of the result.
	expected_measures
		The values of its last column.
	"""

	missing_count: MissingCount
	axis: Axis | None
	expected_column_names: list[str]
	expected_measures: list[float]


COUNT_CASES = [
	CountCase(MissingCount(), None, [COUNT_NAME], [3]),
	CountCase(MissingCount(measure=Measure.RATIO), None, [RATIO_NAME], [0.375]),
	CountCase(MissingCount(), Axis.EACH_ROW, [COUNT_NAME], [0, 2, 1, 0]),
	CountCase(MissingCount(measure=Measure.RATIO), Axis.EACH_ROW, [RATIO_NAME], [0.0, 1.0, 0.5, 0.0]),
	CountCase(MissingCount(), Axis.EACH_COLUMN, [NAMES_COLUMN, COUNT_NAME], [1, 2]),
	CountCase(MissingCount(measure=Measure.RATIO), Axis.EACH_COLUMN, [NAMES_COLUMN, RATIO_NAME], [0.25, 0.5]),
]


@pytest.mark.parametrize("case", COUNT_CASES)
def test_count_frame_missing_counts_along_the_chosen_axis_with_the_chosen_measure(case: CountCase) -> None:
	"""
	Check the columns and the values of each kind of count.

	.. versionadded:: 0.1.0

	Parameters
	----------
	case
		The settings and the expected result.
	"""
	count_frame = count_frame_missing(FRAME, case.missing_count, case.axis)

	column_names = list(count_frame.columns)
	last_column = count_frame.iloc[:, -1]
	measures = last_column.tolist()
	assert column_names == case.expected_column_names
	assert measures == case.expected_measures


def test_count_frame_missing_names_each_counted_column() -> None:
	"""
	Check that a count per column starts with the names of the columns.

	.. versionadded:: 0.1.0
	"""
	count_frame = count_frame_missing(FRAME, MissingCount(), Axis.EACH_COLUMN)

	name_column = count_frame[NAMES_COLUMN]
	names = name_column.tolist()
	assert names == EXPECTED_NAMES


def test_count_frame_missing_gives_a_missing_ratio_without_any_value() -> None:
	"""
	Check that the ratio of a Table without rows is missing.

	.. versionadded:: 0.1.0
	"""
	count_frame = count_frame_missing(EMPTY_FRAME, MissingCount(measure=Measure.RATIO), None)

	ratio_column = count_frame[RATIO_NAME]
	missing_ratios = ratio_column.isna()
	is_missing = bool(missing_ratios.all())
	assert is_missing


def test_count_frame_missing_stores_counts_as_integers_and_ratios_as_decimals() -> None:
	"""
	Check the types of the measure columns.

	.. versionadded:: 0.1.0
	"""
	count_frame = count_frame_missing(FRAME, MissingCount(), None)
	ratio_frame = count_frame_missing(FRAME, MissingCount(measure=Measure.RATIO), None)

	count_column = count_frame[COUNT_NAME]
	ratio_column = ratio_frame[RATIO_NAME]
	count_type = find_column_type(count_column)
	ratio_type = find_column_type(ratio_column)
	assert count_type == Type.INT64
	assert ratio_type == Type.FLOAT64


def test_find_frame_missing_marks_each_missing_value() -> None:
	"""
	Check the grid of missing values, one row per row.

	.. versionadded:: 0.1.0
	"""
	missing_grid = find_frame_missing(FRAME)

	missing_rows = missing_grid.tolist()
	assert missing_rows == EXPECTED_MISSING_GRID


def test_count_axis_missing_counts_each_row_on_the_number_of_columns() -> None:
	"""
	Check the counts per row and the number of values behind them.

	.. versionadded:: 0.1.0
	"""
	counts, value_count = count_axis_missing(MISSING_GRID, Axis.EACH_ROW)

	count_list = counts.tolist()
	assert count_list == EXPECTED_ROW_COUNTS
	assert value_count == COLUMN_COUNT


def test_count_axis_missing_counts_each_column_on_the_number_of_rows() -> None:
	"""
	Check the counts per column and the number of values behind them.

	.. versionadded:: 0.1.0
	"""
	counts, value_count = count_axis_missing(MISSING_GRID, Axis.EACH_COLUMN)

	count_list = counts.tolist()
	assert count_list == EXPECTED_COLUMN_COUNTS
	assert value_count == ROW_COUNT


def test_count_axis_missing_counts_the_whole_table_on_every_value() -> None:
	"""
	Check the single count and the number of values behind it.

	.. versionadded:: 0.1.0
	"""
	counts, value_count = count_axis_missing(MISSING_GRID, None)

	count_list = counts.tolist()
	assert count_list == EXPECTED_TOTAL_COUNTS
	assert value_count == CELL_COUNT


def test_build_name_column_holds_the_column_names_as_texts() -> None:
	"""
	Check the names and the type of the column.

	.. versionadded:: 0.1.0
	"""
	name_column = build_name_column(FRAME)

	names = name_column.tolist()
	name_type = find_column_type(name_column)
	assert names == EXPECTED_NAMES
	assert name_type == Type.TEXT

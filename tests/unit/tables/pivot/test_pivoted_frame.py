"""
Unit tests of the pivot table of the rows of a Table.

.. versionadded:: 0.1.0
"""

from datetime import date
from typing import cast

import numpy
import pandas
import pytest

from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.errors.duplicate_column_error import DuplicateColumnError
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.statistics.count import Count
from numdaplot.statistics.counted_missing import CountedMissing
from numdaplot.statistics.mean import Mean
from numdaplot.statistics.sum import Sum
from numdaplot.tables.aggregation.calculation import Calculation
from numdaplot.tables.pivot.pivot_table import PivotTable
from numdaplot.tables.pivot.pivoted_frame import (
	name_value_columns,
	number_row_groups,
	pivot_frame,
	require_present_pivot_values,
	write_decimal,
)

TRIPS = pandas.DataFrame(
	{
		"hour": [9, 8, 8, 9],
		"day": pandas.Series(["Tue", "Mon", "Tue", "Tue"], dtype="string"),
		"fare": [1.0, 2.0, 3.0, None],
	}
)
TOTAL_FARE = Calculation(column="fare", function=Sum())
MEAN_FARE = Calculation(column="fare", function=Mean())
EVERY_ROW = Calculation(column="fare", function=Count(missing=CountedMissing.INCLUDED))
PRESENT_FARES = Calculation(column="fare", function=Count())
PIVOT_NAMES = ["hour", "Mon", "Tue"]
EXPECTED_HOURS = [8, 9]
EXPECTED_MONDAY_ROWS = [1, 0]
EXPECTED_TUESDAY_ROWS = [1, 2]
EXPECTED_TUESDAY_PRESENT = [1, 1]
EXPECTED_MONDAY_TOTALS = [2.0, 0.0]
EXPECTED_TUESDAY_TOTALS = [3.0, 1.0]
EMPTY_TRIPS = TRIPS.iloc[:0]
MISSING_DAYS = pandas.Series(["Mon", None], dtype="string")
PRESENT_DAYS = pandas.Series(["Mon", "Tue"], dtype="string")
TWO_GROUPS = [numpy.array([0]), numpy.array([1])]
EXPECTED_DAY_NAMES = ["Mon", "Tue"]
DECIMAL_VALUES = pandas.Series([8.0, 2.5])
EXPECTED_DECIMAL_NAMES = ["8", "2.5"]
DAY_VALUES = pandas.Series(pandas.to_datetime([date(2026, 12, 31), date(2027, 1, 1)])).astype("datetime64[s]")
EXPECTED_DATE_NAMES = ["2026-12-31", "2027-01-01"]
WHOLE_DECIMAL = 8.0
WHOLE_DECIMAL_TEXT = "8"
PART_DECIMAL = 2.5
PART_DECIMAL_TEXT = "2.5"
UNKNOWN_NAME = "unknown"
CLASHING_FRAME = pandas.DataFrame(
	{
		"8": [1, 2],
		"hour": pandas.Series([8, 9], dtype="Int64"),
		"fare": [1.0, 2.0],
	}
)
EXPECTED_GROUP_NUMBERS = [1, 0, 1]
THREE_ROWS = 3


def build_pivot(calculation: Calculation) -> PivotTable:
	"""
	Return the pivot table of the trips, one row per hour and one column per day.

	.. versionadded:: 0.1.0

	Parameters
	----------
	calculation
		The statistic of each cell.

	Returns
	-------
	PivotTable
		The settings.
	"""
	pivot = PivotTable(rows=["hour"], columns="day", calculation=calculation)

	return pivot


def test_pivot_frame_gives_one_row_per_group_and_one_column_per_value() -> None:
	"""
	Check the names and the sorted row values of the result.

	.. versionadded:: 0.1.0
	"""
	pivoted = pivot_frame(TRIPS, build_pivot(TOTAL_FARE))

	assert list(pivoted.columns) == PIVOT_NAMES
	assert pivoted["hour"].tolist() == EXPECTED_HOURS


def test_pivot_frame_computes_the_statistic_of_each_cell() -> None:
	"""
	Check that the missing fare is ignored and that an absent combination sums to 0.

	.. versionadded:: 0.1.0
	"""
	pivoted = pivot_frame(TRIPS, build_pivot(TOTAL_FARE))

	assert pivoted["Mon"].tolist() == EXPECTED_MONDAY_TOTALS
	assert pivoted["Tue"].tolist() == EXPECTED_TUESDAY_TOTALS


def test_pivot_frame_gives_a_missing_mean_for_an_absent_combination() -> None:
	"""
	Check that a statistic needing a value gives a missing value without row.

	.. versionadded:: 0.1.0
	"""
	pivoted = pivot_frame(TRIPS, build_pivot(MEAN_FARE))

	monday_means = pivoted["Mon"]
	assert monday_means.isna().tolist() == [False, True]


def test_pivot_frame_counts_the_rows_of_each_cell_when_missing_values_are_included() -> None:
	"""
	Check that the missing fare counts as a row, and that an absent combination counts 0.

	.. versionadded:: 0.1.0
	"""
	pivoted = pivot_frame(TRIPS, build_pivot(EVERY_ROW))

	assert pivoted["Mon"].tolist() == EXPECTED_MONDAY_ROWS
	assert pivoted["Tue"].tolist() == EXPECTED_TUESDAY_ROWS


def test_pivot_frame_leaves_out_the_missing_values_of_a_default_count() -> None:
	"""
	Check that the default Count only counts the present fares.

	.. versionadded:: 0.1.0
	"""
	pivoted = pivot_frame(TRIPS, build_pivot(PRESENT_FARES))

	assert pivoted["Tue"].tolist() == EXPECTED_TUESDAY_PRESENT


def test_pivot_frame_gives_no_row_for_an_empty_table() -> None:
	"""
	Check that an empty Table gives only the row columns, without any row.

	.. versionadded:: 0.1.0
	"""
	pivoted = pivot_frame(EMPTY_TRIPS, build_pivot(TOTAL_FARE))

	assert list(pivoted.columns) == ["hour"]
	assert len(pivoted) == 0


@pytest.mark.parametrize(
	"pivot",
	[
		PivotTable(rows=[UNKNOWN_NAME], columns="day", calculation=TOTAL_FARE),
		PivotTable(rows=["hour"], columns=UNKNOWN_NAME, calculation=TOTAL_FARE),
		PivotTable(rows=["hour"], columns="day", calculation=Calculation(column=UNKNOWN_NAME, function=Sum())),
	],
)
def test_pivot_frame_refuses_an_unknown_column(pivot: PivotTable) -> None:
	"""
	Check every setting naming a column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	pivot
		Settings naming a column the frame does not have.
	"""
	with pytest.raises(ColumnNotFoundError):
		pivot_frame(TRIPS, pivot)


def test_pivot_frame_refuses_a_value_named_like_a_row_column() -> None:
	"""
	Check a value of ``columns`` whose text is the name of a row column.

	.. versionadded:: 0.1.0
	"""
	pivot = PivotTable(rows=["8"], columns="hour", calculation=TOTAL_FARE)

	with pytest.raises(DuplicateColumnError):
		pivot_frame(CLASHING_FRAME, pivot)


def test_pivot_frame_refuses_a_statistic_that_does_not_apply() -> None:
	"""
	Check that the statistic is checked against the type of its column.

	.. versionadded:: 0.1.0
	"""
	day_mean = Calculation(column="day", function=Mean())

	with pytest.raises(IncompatibleTypesError):
		pivot_frame(TRIPS, build_pivot(day_mean))


def test_require_present_pivot_values_accepts_present_values() -> None:
	"""
	Check that a column without missing value passes.

	.. versionadded:: 0.1.0
	"""
	require_present_pivot_values(PRESENT_DAYS, "day")


def test_require_present_pivot_values_points_to_drop_missing() -> None:
	"""
	Check that the message names the column and the method removing the missing values.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError, match="drop_missing with ndp.MissingDrop"):
		require_present_pivot_values(MISSING_DAYS, "day")


def test_name_value_columns_keeps_texts() -> None:
	"""
	Check the names given by a text column.

	.. versionadded:: 0.1.0
	"""
	names = name_value_columns(PRESENT_DAYS, TWO_GROUPS, "day")

	assert names == EXPECTED_DAY_NAMES


def test_name_value_columns_writes_whole_decimals_without_decimal_part() -> None:
	"""
	Check the names given by a decimal column.

	.. versionadded:: 0.1.0
	"""
	names = name_value_columns(DECIMAL_VALUES, TWO_GROUPS, "hour")

	assert names == EXPECTED_DECIMAL_NAMES


def test_name_value_columns_writes_dates_year_first() -> None:
	"""
	Check the names given by a date column.

	.. versionadded:: 0.1.0
	"""
	names = name_value_columns(DAY_VALUES, TWO_GROUPS, "day")

	assert names == EXPECTED_DATE_NAMES


def test_name_value_columns_gives_no_name_without_group() -> None:
	"""
	Check that an empty column gives no name.

	.. versionadded:: 0.1.0
	"""
	names = name_value_columns(PRESENT_DAYS.iloc[:0], [], "day")

	assert names == []


def test_write_decimal_leaves_out_the_decimal_part_of_a_whole_number() -> None:
	"""
	Check a whole decimal.

	.. versionadded:: 0.1.0
	"""
	text = write_decimal(WHOLE_DECIMAL)

	assert text == WHOLE_DECIMAL_TEXT


def test_write_decimal_keeps_the_decimal_part_of_other_numbers() -> None:
	"""
	Check a decimal that is not whole.

	.. versionadded:: 0.1.0
	"""
	text = write_decimal(PART_DECIMAL)

	assert text == PART_DECIMAL_TEXT


def test_number_row_groups_gives_the_group_of_each_row() -> None:
	"""
	Check the number given to each row.

	.. versionadded:: 0.1.0
	"""
	row_groups = [numpy.array([1]), numpy.array([0, 2])]

	group_numbers = number_row_groups(row_groups, THREE_ROWS)

	number_list = cast(list[int], group_numbers.tolist())
	assert number_list == EXPECTED_GROUP_NUMBERS

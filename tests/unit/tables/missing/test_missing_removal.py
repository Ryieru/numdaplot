"""
Unit tests of the removal of the rows or the columns of a Table holding missing values.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

import numpy
import pandas
import pytest

from numdaplot.errors.column_not_found_error import ColumnNotFoundError
from numdaplot.positions.axis import Axis
from numdaplot.tables.missing.missing_drop import MissingDrop
from numdaplot.tables.missing.missing_mode import MissingMode
from numdaplot.tables.missing.missing_ratio import MissingRatio
from numdaplot.tables.missing.missing_removal import (
	drop_frame_missing,
	drop_missing_columns,
	drop_missing_rows,
	find_dropped,
	find_ratio_dropped,
)
from numdaplot.tables.missing.ratio_comparison import RatioComparison

FRAME = pandas.DataFrame(
	{
		"visit": [1.0, 2.0, 3.0, 4.0],
		"price": [120.0, None, None, 90.0],
		"stock": [3.0, None, 5.0, None],
	}
)
EMPTY_FRAME = pandas.DataFrame({"price": pandas.Series(dtype="float64")})
EVERY_NAME = ["visit", "price", "stock"]
EXPECTED_ROW_NUMBERS = [0, 1]
COUNTS = numpy.array([0, 1, 2, 3], dtype=numpy.int64)
VALUE_COUNT = 3
NO_VALUE = 0
HALF_RATIO = 0.5
ONE_THIRD_RATIO = 1 / 3
EXPECTED_NOTHING_DROPPED = [False, False, False, False]
EXPECTED_ANY_DROPPED = [False, True, True, True]
EXPECTED_ALL_DROPPED = [False, False, False, True]
EXPECTED_ABOVE_THIRD_DROPPED = [False, False, True, True]
EXPECTED_EVERY_ROW_NUMBER = [0, 1, 2, 3]
UNKNOWN_NAMES = ["discount"]


@dataclass(frozen=True)
class DropCase:
	"""
	A removal of missing values from FRAME and its expected result.

	.. versionadded:: 0.1.0

	Parameters
	----------
	missing_drop
		The settings of the removal.
	expected_visits
		The visits of the remaining rows.
	expected_names
		The names of the remaining columns.
	"""

	missing_drop: MissingDrop
	expected_visits: list[float]
	expected_names: list[str]


DROP_CASES = [
	DropCase(MissingDrop(), [1.0], EVERY_NAME),
	DropCase(MissingDrop(columns=["price"]), [1.0, 4.0], EVERY_NAME),
	DropCase(MissingDrop(columns=["price", "stock"], rule=MissingMode.ALL), [1.0, 3.0, 4.0], EVERY_NAME),
	DropCase(MissingDrop(rule=MissingRatio(ratio=ONE_THIRD_RATIO)), [1.0], EVERY_NAME),
	DropCase(
		MissingDrop(rule=MissingRatio(ratio=ONE_THIRD_RATIO, comparison=RatioComparison.ABOVE)),
		[1.0, 3.0, 4.0],
		EVERY_NAME,
	),
	DropCase(MissingDrop(axis=Axis.EACH_COLUMN), [1.0, 2.0, 3.0, 4.0], ["visit"]),
	DropCase(MissingDrop(axis=Axis.EACH_COLUMN, columns=["price"]), [1.0, 2.0, 3.0, 4.0], ["visit", "stock"]),
	DropCase(MissingDrop(axis=Axis.EACH_COLUMN, rule=MissingMode.ALL), [1.0, 2.0, 3.0, 4.0], EVERY_NAME),
	DropCase(
		MissingDrop(axis=Axis.EACH_COLUMN, rule=MissingRatio(ratio=HALF_RATIO, comparison=RatioComparison.ABOVE)),
		[1.0, 2.0, 3.0, 4.0],
		EVERY_NAME,
	),
]


def read_visits(frame: pandas.DataFrame) -> list[float]:
	"""
	Return the visit column of the remaining rows.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The remaining rows.

	Returns
	-------
	list[float]
		The visit of each row.
	"""
	visit_column = frame["visit"]
	visits = visit_column.tolist()

	return visits


@pytest.mark.parametrize("case", DROP_CASES)
def test_drop_frame_missing_removes_what_the_settings_choose(case: DropCase) -> None:
	"""
	Check the remaining rows and columns of each kind of removal.

	.. versionadded:: 0.1.0

	Parameters
	----------
	case
		The settings and the expected result.
	"""
	remaining_frame = drop_frame_missing(FRAME, case.missing_drop)

	visits = read_visits(remaining_frame)
	column_names = list(remaining_frame.columns)
	assert visits == case.expected_visits
	assert column_names == case.expected_names


def test_drop_frame_missing_rejects_an_unknown_column() -> None:
	"""
	Check that a looked at column that does not exist raises ColumnNotFoundError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ColumnNotFoundError):
		drop_frame_missing(FRAME, MissingDrop(columns=UNKNOWN_NAMES))


def test_drop_missing_rows_numbers_the_remaining_rows_from_zero() -> None:
	"""
	Check that the remaining rows are renumbered.

	.. versionadded:: 0.1.0
	"""
	remaining_frame = drop_missing_rows(FRAME, FRAME, MissingMode.ALL)

	row_numbers = remaining_frame.index.tolist()
	assert row_numbers == EXPECTED_EVERY_ROW_NUMBER


def test_drop_missing_rows_only_looks_at_the_given_columns() -> None:
	"""
	Check that missing values outside the looked at columns are ignored.

	.. versionadded:: 0.1.0
	"""
	looked_frame = FRAME[["price"]]

	remaining_frame = drop_missing_rows(FRAME, looked_frame, MissingMode.ANY)

	row_numbers = remaining_frame.index.tolist()
	assert row_numbers == EXPECTED_ROW_NUMBERS


def test_drop_missing_columns_keeps_every_column_of_a_table_without_rows() -> None:
	"""
	Check that a Table without rows loses no column, whatever the rule.

	.. versionadded:: 0.1.0
	"""
	remaining_frame = drop_missing_columns(EMPTY_FRAME, EMPTY_FRAME, MissingMode.ALL)

	column_names = list(remaining_frame.columns)
	expected_names = list(EMPTY_FRAME.columns)
	assert column_names == expected_names


def test_find_dropped_drops_nothing_without_any_value() -> None:
	"""
	Check that no row or column is removed when there is no value to count.

	.. versionadded:: 0.1.0
	"""
	dropped = find_dropped(COUNTS, NO_VALUE, MissingMode.ALL)

	dropped_list = dropped.tolist()
	assert dropped_list == EXPECTED_NOTHING_DROPPED


def test_find_dropped_with_any_drops_a_single_missing_value() -> None:
	"""
	Check that MissingMode.ANY removes every count above zero.

	.. versionadded:: 0.1.0
	"""
	dropped = find_dropped(COUNTS, VALUE_COUNT, MissingMode.ANY)

	dropped_list = dropped.tolist()
	assert dropped_list == EXPECTED_ANY_DROPPED


def test_find_dropped_with_all_drops_only_full_counts() -> None:
	"""
	Check that MissingMode.ALL removes only counts equal to the number of values.

	.. versionadded:: 0.1.0
	"""
	dropped = find_dropped(COUNTS, VALUE_COUNT, MissingMode.ALL)

	dropped_list = dropped.tolist()
	assert dropped_list == EXPECTED_ALL_DROPPED


def test_find_ratio_dropped_at_least_includes_the_threshold() -> None:
	"""
	Check that a ratio equal to the threshold is removed with AT_LEAST.

	.. versionadded:: 0.1.0
	"""
	dropped = find_ratio_dropped(COUNTS, VALUE_COUNT, MissingRatio(ratio=ONE_THIRD_RATIO))

	dropped_list = dropped.tolist()
	assert dropped_list == EXPECTED_ANY_DROPPED


def test_find_ratio_dropped_above_excludes_the_threshold() -> None:
	"""
	Check that a ratio equal to the threshold is kept with ABOVE.

	.. versionadded:: 0.1.0
	"""
	above_third = MissingRatio(ratio=ONE_THIRD_RATIO, comparison=RatioComparison.ABOVE)

	dropped = find_ratio_dropped(COUNTS, VALUE_COUNT, above_third)

	dropped_list = dropped.tolist()
	assert dropped_list == EXPECTED_ABOVE_THIRD_DROPPED

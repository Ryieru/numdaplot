"""
Unit tests of the rows a join puts side by side.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
import pytest

import numdaplot as ndp
from numdaplot.tables.joining.joined_rows import (
	add_unmatched_other_rows,
	add_unmatched_rows,
	match_rows,
	number_present_rows,
	pair_rows,
)

KEY_FRAME = pandas.DataFrame({"id": [1.0, 2.0, None, 1.0]})
OTHER_KEY_FRAME = pandas.DataFrame({"id": [3.0, 1.0, None, 1.0]})
EXPECTED_PAIRS = {
	ndp.JoinMode.INNER: ([0, 0, 3, 3], [1, 3, 1, 3]),
	ndp.JoinMode.LEFT: ([0, 0, 1, 2, 3, 3], [1, 3, -1, -1, 1, 3]),
	ndp.JoinMode.RIGHT: ([0, 0, 3, 3, -1, -1], [1, 3, 1, 3, 0, 2]),
	ndp.JoinMode.OUTER: ([0, 0, 1, 2, 3, 3, -1, -1], [1, 3, -1, -1, 1, 3, 0, 2]),
}
TWO_KEY_FRAME = pandas.DataFrame({"id": [1.0, 1.0], "seat": ["A", "B"]})
OTHER_TWO_KEY_FRAME = pandas.DataFrame({"id": [1.0], "seat": ["B"]})
EXPECTED_TWO_KEY_ROWS = ([1], [0])
ROW_LABEL = 1
EXPECTED_PRESENT_ROWS = [0, 1, 3]
EXPECTED_PRESENT_LABELS = [0, ROW_LABEL]
MATCHED_ROWS = numpy.array([1, 1])
MATCHED_OTHER_ROWS = numpy.array([0, 2])
ROW_COUNT = 3
EXPECTED_ALL_ROWS = [0, 1, 1, 2]
EXPECTED_ALL_OTHER_ROWS = [-1, 0, 2, -1]
SINGLE_ROWS = numpy.array([0])
SINGLE_OTHER_ROWS = numpy.array([1])
EXPECTED_OTHER_ROWS_FIRST = [1, 0, 2]
EXPECTED_ROWS_AFTER = [0, -1, -1]


@pytest.mark.parametrize("mode", list(ndp.JoinMode))
def test_pair_rows_keeps_the_rows_of_each_mode(mode: ndp.JoinMode) -> None:
	"""
	Check the pairs of rows of each mode, missing keys never matching.

	.. versionadded:: 0.1.0

	Parameters
	----------
	mode
		Which rows are kept.
	"""
	rows, other_rows = pair_rows(KEY_FRAME, OTHER_KEY_FRAME, mode)

	expected_rows, expected_other_rows = EXPECTED_PAIRS[mode]
	row_list = rows.tolist()
	other_row_list = other_rows.tolist()
	assert row_list == expected_rows
	assert other_row_list == expected_other_rows


def test_match_rows_matches_the_combination_of_several_keys() -> None:
	"""
	Check that two keys match only when both are equal.

	.. versionadded:: 0.1.0
	"""
	rows, other_rows = match_rows(TWO_KEY_FRAME, OTHER_TWO_KEY_FRAME)

	row_list = rows.tolist()
	other_row_list = other_rows.tolist()
	assert (row_list, other_row_list) == EXPECTED_TWO_KEY_ROWS


def test_number_present_rows_leaves_out_rows_with_a_missing_key() -> None:
	"""
	Check that only the rows with every key present remain, numbered after the keys.

	.. versionadded:: 0.1.0
	"""
	present_frame = number_present_rows(KEY_FRAME, ROW_LABEL)

	row_column = present_frame[ROW_LABEL]
	row_list = row_column.tolist()
	labels = present_frame.columns.tolist()
	assert row_list == EXPECTED_PRESENT_ROWS
	assert labels == EXPECTED_PRESENT_LABELS


def test_add_unmatched_rows_places_each_unmatched_row_at_its_row() -> None:
	"""
	Check that the unmatched rows join the matched ones in the order of the joined Table.

	.. versionadded:: 0.1.0
	"""
	rows, other_rows = add_unmatched_rows(MATCHED_ROWS, MATCHED_OTHER_ROWS, ROW_COUNT)

	row_list = rows.tolist()
	other_row_list = other_rows.tolist()
	assert row_list == EXPECTED_ALL_ROWS
	assert other_row_list == EXPECTED_ALL_OTHER_ROWS


def test_add_unmatched_other_rows_places_them_last() -> None:
	"""
	Check that the unmatched rows of the other Table come after every pair, in their order.

	.. versionadded:: 0.1.0
	"""
	other_rows, rows = add_unmatched_other_rows(SINGLE_OTHER_ROWS, SINGLE_ROWS, ROW_COUNT)

	other_row_list = other_rows.tolist()
	row_list = rows.tolist()
	assert other_row_list == EXPECTED_OTHER_ROWS_FIRST
	assert row_list == EXPECTED_ROWS_AFTER

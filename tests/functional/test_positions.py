"""
Functional tests of positions, axes and sort settings, as a user creates them from ndp.

.. versionadded:: 0.1.0
"""

import pytest

import numdaplot as ndp

LAST_POSITION = -1
FIRST_ROW = 0
FIFTH_ROW = 4
EVEN_STEP = 2
SELECTED_COLUMNS = ["total", "prix"]
ZERO_STEP = 0
EXPECTED_AXIS_NAMES = ["EACH_ROW", "EACH_COLUMN"]
EXPECTED_ORDER_NAMES = ["ASCENDING", "DESCENDING"]
EXPECTED_MISSING_POSITION_NAMES = ["FIRST", "LAST"]


def test_a_region_describes_a_block_of_rows_and_named_columns() -> None:
	"""
	Check that a user can describe the first five rows of two named columns.

	.. versionadded:: 0.1.0
	"""
	first_rows = ndp.Range(start=FIRST_ROW, stop=FIFTH_ROW)
	region = ndp.Region(rows=first_rows, columns=SELECTED_COLUMNS)

	assert region.rows == first_rows
	assert region.columns == SELECTED_COLUMNS


def test_a_region_describes_the_last_row() -> None:
	"""
	Check that a user can target the last row with a negative Index.

	.. versionadded:: 0.1.0
	"""
	last_row = ndp.Index(LAST_POSITION)
	region = ndp.Region(rows=last_row)

	assert region.rows == last_row
	assert region.columns is None


def test_a_range_with_a_zero_step_is_rejected() -> None:
	"""
	Check that a user giving a zero step gets InvalidStepError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidStepError):
		ndp.Range(start=FIRST_ROW, stop=FIFTH_ROW, step=ZERO_STEP)


def test_a_range_can_exclude_its_end() -> None:
	"""
	Check that a user can exclude the end of a range, as in Python.

	.. versionadded:: 0.1.0
	"""
	sequence = ndp.Range(start=FIRST_ROW, stop=FIFTH_ROW, step=EVEN_STEP, bounds=ndp.Bounds.LOW_ONLY)

	assert sequence.bounds == ndp.Bounds.LOW_ONLY


def test_axis_order_and_missing_position_offer_their_choices() -> None:
	"""
	Check the members of the axis and sort enums exposed by ndp.

	.. versionadded:: 0.1.0
	"""
	axis_names = [axis.name for axis in ndp.Axis]
	order_names = [order.name for order in ndp.Order]
	position_names = [position.name for position in ndp.MissingPosition]

	assert axis_names == EXPECTED_AXIS_NAMES
	assert order_names == EXPECTED_ORDER_NAMES
	assert position_names == EXPECTED_MISSING_POSITION_NAMES

"""
Unit tests of CellOutOfRangeError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.cell_out_of_range_error import CellOutOfRangeError
from numdaplot.errors.numdaplot_error import NumdaplotError

ROW = 2
COLUMN = 0
ROW_COUNT = 2
COLUMN_COUNT = 2
EXPECTED_MESSAGE = "Cell (2, 0) is outside a Layout of 2 rows and 2 columns."


def test_cell_out_of_range_error_is_a_numdaplot_error() -> None:
	"""
	Check that CellOutOfRangeError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(CellOutOfRangeError, NumdaplotError)


def test_cell_out_of_range_error_message_states_the_cell_and_the_layout() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = CellOutOfRangeError(ROW, COLUMN, ROW_COUNT, COLUMN_COUNT)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_cell_out_of_range_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = CellOutOfRangeError(ROW, COLUMN, ROW_COUNT, COLUMN_COUNT)

	assert error.row == ROW
	assert error.column == COLUMN
	assert error.row_count == ROW_COUNT
	assert error.column_count == COLUMN_COUNT

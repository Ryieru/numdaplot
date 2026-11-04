"""
Unit tests of OccupiedCellError.

.. versionadded:: 0.1.0
"""

from numdaplot.errors.numdaplot_error import NumdaplotError
from numdaplot.errors.occupied_cell_error import OccupiedCellError

ROW = 0
COLUMN = 1
EXPECTED_MESSAGE = "Cell (0, 1) already holds a Plot."


def test_occupied_cell_error_is_a_numdaplot_error() -> None:
	"""
	Check that OccupiedCellError is caught by NumdaplotError.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(OccupiedCellError, NumdaplotError)


def test_occupied_cell_error_message_states_the_occupied_cell() -> None:
	"""
	Check the message built from the error values.

	.. versionadded:: 0.1.0
	"""
	error = OccupiedCellError(ROW, COLUMN)

	error_text = str(error)
	assert error_text == EXPECTED_MESSAGE


def test_occupied_cell_error_keeps_its_values() -> None:
	"""
	Check that the values given to the error are available as attributes.

	.. versionadded:: 0.1.0
	"""
	error = OccupiedCellError(ROW, COLUMN)

	assert error.row == ROW
	assert error.column == COLUMN

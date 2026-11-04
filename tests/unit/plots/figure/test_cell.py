"""
Unit tests of Cell.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.invalid_count_error import InvalidCountError
from numdaplot.plots.figure.cell import Cell


def test_cell_spans_a_single_cell_by_default() -> None:
	"""
	Check the default spans.

	.. versionadded:: 0.1.0
	"""
	cell = Cell(row=1, column=2)

	assert cell.row_span == 1
	assert cell.column_span == 1


def test_cell_rejects_a_row_span_of_zero() -> None:
	"""
	Check that a row span of 0 raises InvalidCountError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidCountError):
		Cell(row=0, column=0, row_span=0)


def test_cell_rejects_a_column_span_of_zero() -> None:
	"""
	Check that a column span of 0 raises InvalidCountError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidCountError):
		Cell(row=0, column=0, column_span=0)

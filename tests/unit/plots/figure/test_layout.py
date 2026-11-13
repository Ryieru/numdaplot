"""
Unit tests of Layout.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.settings.invalid_count_error import InvalidCountError
from numdaplot.plots.figure.layout import Layout


def test_layout_keeps_its_rows_and_columns() -> None:
	"""
	Check that a grid of one cell is accepted.

	.. versionadded:: 0.1.0
	"""
	layout = Layout(rows=1, columns=1)

	assert layout.rows == 1
	assert layout.columns == 1


def test_layout_rejects_no_row() -> None:
	"""
	Check that 0 rows raise InvalidCountError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidCountError):
		Layout(rows=0, columns=2)


def test_layout_rejects_no_column() -> None:
	"""
	Check that 0 columns raise InvalidCountError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidCountError):
		Layout(rows=2, columns=0)

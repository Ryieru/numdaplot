"""
Unit tests of find_numpy_axis.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.dimension_error import DimensionError
from numdaplot.positions.axis import Axis
from numdaplot.positions.axis_number import find_numpy_axis

TWO_DIMENSIONS = 2
ONE_DIMENSION = 1
ROW_AXIS_NUMBER = 1
COLUMN_AXIS_NUMBER = 0


def test_find_numpy_axis_runs_each_row_along_the_columns() -> None:
	"""
	Check that EACH_ROW gives the numpy axis 1.

	.. versionadded:: 0.1.0
	"""
	numpy_axis = find_numpy_axis(Axis.EACH_ROW, TWO_DIMENSIONS)

	assert numpy_axis == ROW_AXIS_NUMBER


def test_find_numpy_axis_runs_each_column_along_the_rows() -> None:
	"""
	Check that EACH_COLUMN gives the numpy axis 0.

	.. versionadded:: 0.1.0
	"""
	numpy_axis = find_numpy_axis(Axis.EACH_COLUMN, TWO_DIMENSIONS)

	assert numpy_axis == COLUMN_AXIS_NUMBER


def test_find_numpy_axis_gives_none_without_axis() -> None:
	"""
	Check that an omitted axis stays omitted, whatever the number of dimensions.

	.. versionadded:: 0.1.0
	"""
	numpy_axis = find_numpy_axis(None, ONE_DIMENSION)

	assert numpy_axis is None


def test_find_numpy_axis_rejects_an_axis_on_one_dimension() -> None:
	"""
	Check that an axis on a one-dimensional Array raises DimensionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DimensionError):
		find_numpy_axis(Axis.EACH_ROW, ONE_DIMENSION)

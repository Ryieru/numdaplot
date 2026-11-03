"""
Unit tests of the columns built from Arrays.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.arrays.array import Array
from numdaplot.errors.dimension_error import DimensionError
from numdaplot.errors.empty_list_error import EmptyListError
from numdaplot.errors.invalid_column_name_error import InvalidColumnNameError
from numdaplot.errors.shape_mismatch_error import ShapeMismatchError
from numdaplot.tables.frames.array_frame import build_array_frame

CITIES = Array.from_list(["Pau", "Lyon"])
PRICES = Array.from_list([1.5, 8.0])
SHORT_PRICES = Array.from_list([1.5])
GRID = Array.from_list([[1, 2], [3, 4]])
EXPECTED_COLUMN_NAMES = ["city", "price"]
EXPECTED_DTYPE_NAMES = ["string", "float64"]
EMPTY_NAME = ""


def test_build_array_frame_keeps_the_order_and_types_of_the_arrays() -> None:
	"""
	Check the names and the dtypes of the columns.

	.. versionadded:: 0.1.0
	"""
	frame = build_array_frame({"city": CITIES, "price": PRICES})

	column_names = frame.columns.tolist()
	dtype_names = [str(dtype) for dtype in frame.dtypes]
	assert column_names == EXPECTED_COLUMN_NAMES
	assert dtype_names == EXPECTED_DTYPE_NAMES


def test_build_array_frame_rejects_no_column() -> None:
	"""
	Check that an empty dictionary raises EmptyListError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(EmptyListError):
		build_array_frame({})


def test_build_array_frame_rejects_an_empty_name() -> None:
	"""
	Check that an empty column name raises InvalidColumnNameError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidColumnNameError):
		build_array_frame({EMPTY_NAME: PRICES})


def test_build_array_frame_rejects_a_two_dimensional_array() -> None:
	"""
	Check that a grid raises DimensionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(DimensionError):
		build_array_frame({"grid": GRID})


def test_build_array_frame_rejects_arrays_of_different_lengths() -> None:
	"""
	Check that Arrays of two and one values raise ShapeMismatchError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ShapeMismatchError):
		build_array_frame({"city": CITIES, "price": SHORT_PRICES})

"""
Unit tests of ArrayLayout.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from typing import Any, cast

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays import array_layout
from numdaplot.arrays.array_layout import ArrayLayout
from numdaplot.arrays.array_sorting import ArraySorting
from numdaplot.arrays.shape import Shape
from numdaplot.errors.shape_mismatch_error import ShapeMismatchError
from numdaplot.positions.axis import Axis

SORT_VALUES_NAME = "sort_values"
FIND_UNIQUE_VALUES_NAME = "find_unique_values"
LINE = [1, 2, 3, 4, 5, 6]
GRID_SHAPE = Shape([2, 3])
EXPECTED_GRID = [[1, 2, 3], [4, 5, 6]]
WRONG_SHAPE = Shape([4, 2])
GRID = [[1, 2, 3], [4, 5, 6]]
EXPECTED_TRANSPOSED_GRID = [[1, 4], [2, 5], [3, 6]]
EXPECTED_FLAT_VALUES = [1, 2, 3, 4, 5, 6]
FAKE_VALUES = numpy.array([9, 9])
EXPECTED_FAKE_VALUES = [9, 9]


def give_fake_values(*arguments: Any) -> NDArray[Any]:
	"""
	Fake value builder returning known values whatever it receives.

	.. versionadded:: 0.1.0

	Parameters
	----------
	*arguments
		The arguments of the replaced function, ignored.

	Returns
	-------
	NDArray
		Always the fake values.
	"""
	return FAKE_VALUES


def read_values(array: ArrayLayout) -> list[Any]:
	"""
	Return the values of an Array as a Python list.

	.. versionadded:: 0.1.0

	Parameters
	----------
	array
		The Array.

	Returns
	-------
	list[Any]
		Its values.
	"""
	numpy_values = array.to_numpy()
	raw_values = numpy_values.tolist()
	value_list = cast(list[Any], raw_values)

	return value_list


def test_reshape_arranges_the_values_in_reading_order() -> None:
	"""
	Check that six values become two rows of three.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(LINE)
	array = ArrayLayout._create(values)

	reshaped_array = array.reshape(GRID_SHAPE)

	reshaped_values = read_values(reshaped_array)
	assert reshaped_values == EXPECTED_GRID


def test_reshape_rejects_another_number_of_values() -> None:
	"""
	Check that six values cannot fill a shape of eight.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(LINE)
	array = ArrayLayout._create(values)

	with pytest.raises(ShapeMismatchError):
		array.reshape(WRONG_SHAPE)


def test_transpose_turns_rows_into_columns() -> None:
	"""
	Check that two rows of three become three rows of two.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	array = ArrayLayout._create(values)

	transposed_array = array.transpose()

	transposed_values = read_values(transposed_array)
	assert transposed_values == EXPECTED_TRANSPOSED_GRID


def test_flatten_reads_the_values_in_one_dimension() -> None:
	"""
	Check that a grid becomes a line, row after row.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	array = ArrayLayout._create(values)

	flat_array = array.flatten()

	flat_values = read_values(flat_array)
	assert flat_values == EXPECTED_FLAT_VALUES


def test_sort_returns_the_sorted_values(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that sort returns what the sorting gives.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the sorting with a fake.
	"""
	monkeypatch.setattr(array_layout, SORT_VALUES_NAME, give_fake_values)
	values = numpy.array(LINE)
	array = ArrayLayout._create(values)

	sorted_array = array.sort(ArraySorting())

	sorted_values = read_values(sorted_array)
	assert sorted_values == EXPECTED_FAKE_VALUES


def test_unique_returns_the_distinct_values(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that unique returns what the search for distinct values gives.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the search for distinct values with a fake.
	"""
	monkeypatch.setattr(array_layout, FIND_UNIQUE_VALUES_NAME, give_fake_values)
	values = numpy.array(LINE)
	array = ArrayLayout._create(values)

	unique_array = array.unique()

	unique_values = read_values(unique_array)
	assert unique_values == EXPECTED_FAKE_VALUES


def test_sort_without_settings_sorts_with_the_default_sorting(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that sort without settings hands the default ArraySorting and no axis to the sorting.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the sorting with a recorder.
	"""
	received_settings = list[tuple[ArraySorting, Axis | None]]()

	def sort_recorded_values(values: NDArray[Any], sorting: ArraySorting, axis: Axis | None) -> NDArray[Any]:
		"""
		Keep the sorting and the axis, and return the fake values.

		.. versionadded:: 0.1.0

		Parameters
		----------
		values
			The values, ignored.
		sorting
			The sorting received.
		axis
			The axis received.

		Returns
		-------
		NDArray
			Always the fake values.
		"""
		received_settings.append((sorting, axis))

		return FAKE_VALUES

	monkeypatch.setattr(array_layout, SORT_VALUES_NAME, sort_recorded_values)
	values = numpy.array(LINE)
	array = ArrayLayout._create(values)

	array.sort()

	assert received_settings == [(ArraySorting(), None)]

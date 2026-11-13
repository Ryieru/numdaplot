"""
Unit tests of ArrayCreation.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays import array_creation
from numdaplot.arrays.array_creation import ArrayCreation
from numdaplot.arrays.array_data import read_stored_values
from numdaplot.arrays.creation.random_integers import RandomIntegers
from numdaplot.arrays.creation.spacing import Spacing
from numdaplot.positions.range import Range
from numdaplot.positions.shape import Shape

FAKE_VALUES = numpy.array([7, 8, 9])
EXPECTED_FAKE_VALUES = [7, 8, 9]
NUMPY_VALUES = [1, 2]
CHANGED_VALUE = 99
FIRST_POSITION = 0
LIST_VALUES = [1, 2]
SHAPE = Shape([3])
FILL_VALUE = 0
SEQUENCE = Range(start=0, stop=2)
SPACING = Spacing(start=0, stop=1, count=3)
DIE = RandomIntegers(low=1, high=6)
SEED = 0
DRAW_RANDOM_VALUES_NAME = "draw_random_values"
COMPUTE_SPACING_VALUES_NAME = "compute_spacing_values"
COMPUTE_RANGE_VALUES_NAME = "compute_range_values"
BUILD_FILLED_VALUES_NAME = "build_filled_values"
CONVERT_LIST_NAME = "convert_list"


def give_fake_values(*arguments: Any) -> NDArray[Any]:
	"""
	Fake value builder returning known values whatever it receives.

	.. versionadded:: 0.1.0

	Parameters
	----------
	*arguments
		The arguments of the replaced builder, ignored.

	Returns
	-------
	NDArray
		Always the fake values.
	"""
	return FAKE_VALUES


def read_values(created_array: ArrayCreation) -> list[Any]:
	"""
	Return the values of a created Array as a Python list.

	.. versionadded:: 0.1.0

	Parameters
	----------
	created_array
		The created Array.

	Returns
	-------
	list[Any]
		Its values.
	"""
	numpy_values = read_stored_values(created_array)
	raw_values = numpy_values.tolist()
	value_list = cast(list[Any], raw_values)

	return value_list


def test_from_list_stores_the_converted_list(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that from_list stores what the list conversion returns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the list conversion with a fake.
	"""
	monkeypatch.setattr(array_creation, CONVERT_LIST_NAME, give_fake_values)

	created_array = ArrayCreation.from_list(LIST_VALUES)

	value_list = read_values(created_array)
	assert value_list == EXPECTED_FAKE_VALUES


def test_from_numpy_is_independent_from_the_numpy_array() -> None:
	"""
	Check that changing the numpy array afterwards never changes the Array.

	.. versionadded:: 0.1.0
	"""
	numpy_values = numpy.array(NUMPY_VALUES)
	created_array = ArrayCreation.from_numpy(numpy_values)

	numpy_values[FIRST_POSITION] = CHANGED_VALUE

	value_list = read_values(created_array)
	assert value_list == NUMPY_VALUES


def test_filled_stores_the_filled_values(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that filled stores what the filled value builder returns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the filled value builder with a fake.
	"""
	monkeypatch.setattr(array_creation, BUILD_FILLED_VALUES_NAME, give_fake_values)

	created_array = ArrayCreation.filled(SHAPE, FILL_VALUE)

	value_list = read_values(created_array)
	assert value_list == EXPECTED_FAKE_VALUES


def test_from_range_stores_the_range_values(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that from_range stores what the range computation returns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the range computation with a fake.
	"""
	monkeypatch.setattr(array_creation, COMPUTE_RANGE_VALUES_NAME, give_fake_values)

	created_array = ArrayCreation.from_range(SEQUENCE)

	value_list = read_values(created_array)
	assert value_list == EXPECTED_FAKE_VALUES


def test_from_spacing_stores_the_spacing_values(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that from_spacing stores what the spacing computation returns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the spacing computation with a fake.
	"""
	monkeypatch.setattr(array_creation, COMPUTE_SPACING_VALUES_NAME, give_fake_values)

	created_array = ArrayCreation.from_spacing(SPACING)

	value_list = read_values(created_array)
	assert value_list == EXPECTED_FAKE_VALUES


def test_random_stores_the_drawn_values(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that random stores what the random draw returns.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the random draw with a fake.
	"""
	monkeypatch.setattr(array_creation, DRAW_RANDOM_VALUES_NAME, give_fake_values)

	created_array = ArrayCreation.random(DIE, SHAPE, SEED)

	value_list = read_values(created_array)
	assert value_list == EXPECTED_FAKE_VALUES

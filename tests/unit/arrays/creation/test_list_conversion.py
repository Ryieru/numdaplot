"""
Unit tests of the conversion of Python lists to numpy values.

.. versionadded:: 0.1.0
"""

import math
from datetime import date, time

import numpy
import pytest

from numdaplot.arrays.creation import list_conversion
from numdaplot.arrays.creation.list_conversion import (
	choose_stored_type,
	convert_list,
	guess_list_type,
	mark_missing_values,
	store_time_values,
	store_values,
)
from numdaplot.errors.missing_type_error import MissingTypeError
from numdaplot.errors.unsupported_missing_error import UnsupportedMissingError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.types.type import Type

GRID_VALUES = list[object]([[1, 2], [3, 4]])
GRID_DIMENSIONS = (2, 3)
FAKE_DIMENSIONS = (2, 3)
FAKE_SINGLE_VALUES = list[object]([1, 2, 3, 4, 5, 6])
MIXED_NUMBERS = list[object]([1, None, 2.5])
MISSING_ONLY = list[object]([None, None])
DECIMALS_WITH_MISSING = list[object]([1.5, None])
INTEGERS_WITH_MISSING = list[object]([1, None])
DATES_WITH_MISSING = list[object]([date(2026, 1, 31), None])
PRESENT_INTEGERS = list[object]([1, 2])
DECIMALS = list[object]([1.5, 2.5])
TOO_LARGE_INT8 = list[object]([300])
NEGATIVE_INTEGERS = list[object]([-1, 2])
UNSIGNED_DTYPE = numpy.dtype(numpy.uint8)
EMPTY_VALUES = list[object]()
MISSING_POSITION = 1
FIND_LIST_SHAPE_NAME = "find_list_shape"
NOT_A_TIME_TEXT = "NaT"
FLATTEN_LIST_NAME = "flatten_list"
TIME_DTYPE_NAME = "timedelta64[us]"
TIMES_WITH_MISSING = [time(8), None]


def test_convert_list_keeps_the_nesting_as_dimensions() -> None:
	"""
	Check that a list of rows gives a two-dimensional array.

	.. versionadded:: 0.1.0
	"""
	values = convert_list(GRID_VALUES, None)

	value_rows = values.tolist()
	assert value_rows == GRID_VALUES


def test_convert_list_reshapes_the_values_to_the_found_shape(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that the flat values are arranged in the shape found for the list.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the shape and flattening steps with fakes giving six values in two rows of three.
	"""
	monkeypatch.setattr(list_conversion, FIND_LIST_SHAPE_NAME, give_fake_dimensions)
	monkeypatch.setattr(list_conversion, FLATTEN_LIST_NAME, give_fake_single_values)

	values = convert_list(GRID_VALUES, None)

	assert values.shape == GRID_DIMENSIONS


def test_guess_list_type_ignores_missing_values() -> None:
	"""
	Check that integers, decimals and None give FLOAT64.

	.. versionadded:: 0.1.0
	"""
	guessed_type = guess_list_type(MIXED_NUMBERS)

	assert guessed_type == Type.FLOAT64


def test_guess_list_type_gives_none_without_present_value() -> None:
	"""
	Check that only missing values give no type.

	.. versionadded:: 0.1.0
	"""
	guessed_type = guess_list_type(MISSING_ONLY)

	assert guessed_type is None


def test_choose_stored_type_prefers_the_given_type() -> None:
	"""
	Check that a given type wins over the guessed one.

	.. versionadded:: 0.1.0
	"""
	stored_type = choose_stored_type(Type.INT64, Type.FLOAT32)

	assert stored_type == Type.FLOAT32


def test_choose_stored_type_uses_the_guessed_type_when_none_is_given() -> None:
	"""
	Check that the guessed type is used when dtype is omitted.

	.. versionadded:: 0.1.0
	"""
	stored_type = choose_stored_type(Type.TEXT, None)

	assert stored_type == Type.TEXT


def test_choose_stored_type_rejects_two_missing_types() -> None:
	"""
	Check that no guessed and no given type raise MissingTypeError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(MissingTypeError):
		choose_stored_type(None, None)


def test_mark_missing_values_uses_nan_for_decimals() -> None:
	"""
	Check that None becomes NaN in a decimal list.

	.. versionadded:: 0.1.0
	"""
	marked_values = mark_missing_values(DECIMALS_WITH_MISSING, Type.FLOAT64)

	missing_marker = marked_values[MISSING_POSITION]
	assert isinstance(missing_marker, float)
	is_nan = math.isnan(missing_marker)
	assert is_nan


def test_mark_missing_values_uses_nat_for_dates() -> None:
	"""
	Check that None becomes NaT in a date list.

	.. versionadded:: 0.1.0
	"""
	marked_values = mark_missing_values(DATES_WITH_MISSING, Type.DATE)

	missing_marker = marked_values[MISSING_POSITION]
	marker_text = str(missing_marker)
	assert marker_text == NOT_A_TIME_TEXT


def test_mark_missing_values_rejects_a_missing_integer() -> None:
	"""
	Check that INT64 values cannot hold None.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(UnsupportedMissingError):
		mark_missing_values(INTEGERS_WITH_MISSING, Type.INT64)


def test_store_values_widens_integers_to_decimals() -> None:
	"""
	Check that integers can be stored as FLOAT64.

	.. versionadded:: 0.1.0
	"""
	values = store_values(PRESENT_INTEGERS, Type.INT64, Type.FLOAT64)

	assert values.dtype == numpy.float64


def test_store_values_rejects_decimals_stored_as_integers() -> None:
	"""
	Check that decimals cannot be stored as INT64.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError):
		store_values(DECIMALS, Type.FLOAT64, Type.INT64)


def test_store_values_rejects_a_value_out_of_range() -> None:
	"""
	Check that 300 cannot be stored as INT8.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError):
		store_values(TOO_LARGE_INT8, Type.INT64, Type.INT8)


def test_store_values_stores_integers_as_unsigned_integers() -> None:
	"""
	Check that positive integers can be stored as UINT8.

	.. versionadded:: 0.1.0
	"""
	values = store_values(PRESENT_INTEGERS, Type.INT64, Type.UINT8)

	value_list = values.tolist()
	assert values.dtype == UNSIGNED_DTYPE
	assert value_list == PRESENT_INTEGERS


def test_store_values_rejects_a_negative_unsigned_integer() -> None:
	"""
	Check that -1 cannot be stored as UINT8.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError):
		store_values(NEGATIVE_INTEGERS, Type.INT64, Type.UINT8)


def test_store_values_stores_an_empty_list_in_the_given_type() -> None:
	"""
	Check that no value at all gives an empty array of the stored type.

	.. versionadded:: 0.1.0
	"""
	values = store_values(EMPTY_VALUES, None, Type.INT32)

	assert values.dtype == numpy.int32


def give_fake_dimensions(values: list[object]) -> tuple[int, ...]:
	"""
	Fake shape step giving two rows of three values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The list, ignored.

	Returns
	-------
	tuple[int, ...]
		Always two rows of three.
	"""
	return FAKE_DIMENSIONS


def give_fake_single_values(values: list[object]) -> list[object]:
	"""
	Fake flattening step giving six integers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The list, ignored.

	Returns
	-------
	list[object]
		Always six integers.
	"""
	return FAKE_SINGLE_VALUES


def test_convert_list_stores_times_in_microseconds() -> None:
	"""
	Check that times of day and None give TIME with NaT.

	.. versionadded:: 0.1.0
	"""
	stored_values = convert_list(list(TIMES_WITH_MISSING), None)

	assert stored_values.dtype.name == TIME_DTYPE_NAME


@pytest.mark.parametrize(("guessed_type", "stored_type"), [(Type.TIME, Type.DURATION), (Type.INT64, Type.TIME)])
def test_store_time_values_refuses_another_type(guessed_type: Type, stored_type: Type) -> None:
	"""
	Check that times are not stored as durations, nor integers as times.

	.. versionadded:: 0.1.0

	Parameters
	----------
	guessed_type
		The type of the values.
	stored_type
		The type asked.
	"""
	with pytest.raises(ValueConversionError):
		store_time_values(list(TIMES_WITH_MISSING), guessed_type, stored_type)

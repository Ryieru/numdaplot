"""
Unit tests of the conversion between ndp.Type and numpy dtypes.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pytest

from numdaplot.errors.types.unsupported_type_error import UnsupportedTypeError
from numdaplot.types.library import Library
from numdaplot.types.numpy_mapping import find_datetime_type, find_duration_type, from_numpy_dtype, to_numpy_dtype
from numdaplot.types.type import Type

NUMPY_COMPATIBLE_TYPES = [data_type for data_type in Type if data_type != Type.CATEGORY]
FIXED_LENGTH_TEXT_DTYPE = numpy.dtype("<U5")
# Some versions of the numpy stubs leave out the missing value marker of StringDType.
STRING_DTYPE_CLASS = cast(Any, numpy.dtypes.StringDType)
VARIABLE_LENGTH_TEXT_DTYPE = STRING_DTYPE_CLASS(na_object=numpy.nan)
SECOND_DURATION_DTYPE = numpy.dtype("timedelta64[s]")
DAY_DATETIME_DTYPE = numpy.dtype("datetime64[D]")
SECOND_DATETIME_DTYPE = numpy.dtype("datetime64[s]")
COMPLEX_DTYPE = numpy.dtype("complex128")
OBJECT_DTYPE = numpy.dtype("object")
TIME_NUMPY_DTYPE = numpy.dtype("timedelta64[us]")
SECOND_NUMPY_DTYPE = numpy.dtype("timedelta64[s]")


def test_to_numpy_dtype_converts_int32() -> None:
	"""
	Check that INT32 gives the numpy int32 dtype.

	.. versionadded:: 0.1.0
	"""
	numpy_dtype = to_numpy_dtype(Type.INT32)

	expected_dtype = numpy.dtype(numpy.int32)
	assert numpy_dtype == expected_dtype


def test_to_numpy_dtype_converts_text_to_variable_length_strings() -> None:
	"""
	Check that TEXT gives the variable-length StringDType with NaN as missing value.

	.. versionadded:: 0.1.0
	"""
	numpy_dtype = to_numpy_dtype(Type.TEXT)

	assert numpy_dtype == VARIABLE_LENGTH_TEXT_DTYPE


def test_to_numpy_dtype_converts_date_to_day_datetimes() -> None:
	"""
	Check that DATE gives datetime64 with a day unit.

	.. versionadded:: 0.1.0
	"""
	numpy_dtype = to_numpy_dtype(Type.DATE)

	assert numpy_dtype == DAY_DATETIME_DTYPE


def test_to_numpy_dtype_rejects_category() -> None:
	"""
	Check that CATEGORY, which numpy does not have, raises an error naming numpy.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(UnsupportedTypeError) as error_info:
		to_numpy_dtype(Type.CATEGORY)

	assert error_info.value.library == Library.NUMPY


@pytest.mark.parametrize("data_type", NUMPY_COMPATIBLE_TYPES)
def test_from_numpy_dtype_reverses_to_numpy_dtype(data_type: Type) -> None:
	"""
	Check that converting a type to numpy and back gives the same type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data_type
		A type that numpy supports.
	"""
	numpy_dtype = to_numpy_dtype(data_type)
	round_trip_type = from_numpy_dtype(numpy_dtype)

	assert round_trip_type == data_type


def test_from_numpy_dtype_reads_fixed_length_strings_as_text() -> None:
	"""
	Check that the fixed-length strings numpy creates from a list of texts give TEXT.

	.. versionadded:: 0.1.0
	"""
	data_type = from_numpy_dtype(FIXED_LENGTH_TEXT_DTYPE)

	assert data_type == Type.TEXT


def test_from_numpy_dtype_reads_any_duration_unit_as_duration() -> None:
	"""
	Check that a timedelta64 dtype with a unit other than nanoseconds gives DURATION.

	.. versionadded:: 0.1.0
	"""
	data_type = from_numpy_dtype(SECOND_DURATION_DTYPE)

	assert data_type == Type.DURATION


@pytest.mark.parametrize("numpy_dtype", [COMPLEX_DTYPE, OBJECT_DTYPE])
def test_from_numpy_dtype_rejects_dtypes_without_equivalent(numpy_dtype: numpy.dtype[numpy.generic]) -> None:
	"""
	Check that complex numbers and Python objects raise an error.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numpy_dtype
		A numpy dtype that numdaplot does not support.
	"""
	with pytest.raises(UnsupportedTypeError):
		from_numpy_dtype(numpy_dtype)


def test_find_datetime_type_reads_the_day_unit_as_date() -> None:
	"""
	Check that a datetime64 with a day unit gives DATE.

	.. versionadded:: 0.1.0
	"""
	data_type = find_datetime_type(DAY_DATETIME_DTYPE)

	assert data_type == Type.DATE


def test_find_datetime_type_reads_other_units_as_datetime() -> None:
	"""
	Check that a datetime64 with a second unit gives DATETIME.

	.. versionadded:: 0.1.0
	"""
	data_type = find_datetime_type(SECOND_DATETIME_DTYPE)

	assert data_type == Type.DATETIME


def test_find_duration_type_reads_microseconds_as_times() -> None:
	"""
	Check that microseconds give TIME and seconds DURATION.

	.. versionadded:: 0.1.0
	"""
	time_type = find_duration_type(TIME_NUMPY_DTYPE)
	duration_type = find_duration_type(SECOND_NUMPY_DTYPE)

	assert time_type == Type.TIME
	assert duration_type == Type.DURATION


def test_to_numpy_dtype_stores_times_in_microseconds() -> None:
	"""
	Check the storage of TIME and its reverse mapping.

	.. versionadded:: 0.1.0
	"""
	numpy_dtype = to_numpy_dtype(Type.TIME)

	time_type = from_numpy_dtype(numpy_dtype)
	assert numpy_dtype == TIME_NUMPY_DTYPE
	assert time_type == Type.TIME

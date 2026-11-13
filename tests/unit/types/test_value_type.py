"""
Unit tests of find_value_type, find_type_width and find_common_type.

.. versionadded:: 0.1.0
"""

from datetime import UTC, date, datetime, time, timedelta

import numpy
import pytest

from numdaplot.errors.dates.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.types.unsupported_type_error import UnsupportedTypeError
from numdaplot.types.type import Type
from numdaplot.types.value_type import find_common_type, find_type_width, find_value_type

OPERATION = "from_list"
PYTHON_VALUE_TYPES = [
	(True, Type.BOOL),
	(3, Type.INT64),
	(numpy.int8(3), Type.INT64),
	(2.5, Type.FLOAT64),
	("Paris", Type.TEXT),
	(datetime(2026, 1, 31, 8, 30), Type.DATETIME),
	(date(2026, 1, 31), Type.DATE),
	(timedelta(hours=1), Type.DURATION),
]
COMPLEX_VALUE = 1j
EXPECTED_COMPLEX_MESSAGE = "The type complex has no equivalent between numdaplot and numpy."
WIDE_TYPE_WIDTH = 1
NARROW_TYPE_WIDTH = 0
UTC_DATETIME = datetime(2026, 1, 31, 8, 30, tzinfo=UTC)
AFTERNOON = time(15, 35)
ZONED_AFTERNOON = time(15, 35, tzinfo=UTC)


@pytest.mark.parametrize(("value", "expected_type"), PYTHON_VALUE_TYPES)
def test_find_value_type_recognizes_each_python_type(value: object, expected_type: Type) -> None:
	"""
	Check the type of each supported kind of single value, booleans and datetimes included.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		A single value.
	expected_type
		Its numdaplot type.
	"""
	value_type = find_value_type(value)

	assert value_type == expected_type


def test_find_value_type_rejects_a_complex_number() -> None:
	"""
	Check that a value without numdaplot type raises UnsupportedTypeError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(UnsupportedTypeError, match=EXPECTED_COMPLEX_MESSAGE):
		find_value_type(COMPLEX_VALUE)


def test_find_type_width_ranks_decimals_above_integers() -> None:
	"""
	Check that FLOAT64 is wider than INT64.

	.. versionadded:: 0.1.0
	"""
	decimal_width = find_type_width(Type.FLOAT64)
	integer_width = find_type_width(Type.INT64)

	assert decimal_width == WIDE_TYPE_WIDTH
	assert integer_width == NARROW_TYPE_WIDTH


def test_find_common_type_widens_integers_to_decimals() -> None:
	"""
	Check that integers mixed with decimals give FLOAT64.

	.. versionadded:: 0.1.0
	"""
	common_type = find_common_type([Type.INT64, Type.FLOAT64, Type.INT64], OPERATION)

	assert common_type == Type.FLOAT64


def test_find_common_type_widens_dates_to_datetimes() -> None:
	"""
	Check that dates mixed with datetimes give DATETIME.

	.. versionadded:: 0.1.0
	"""
	common_type = find_common_type([Type.DATE, Type.DATETIME], OPERATION)

	assert common_type == Type.DATETIME


def test_find_common_type_rejects_two_families() -> None:
	"""
	Check that a boolean mixed with an integer raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IncompatibleTypesError):
		find_common_type([Type.BOOL, Type.INT64], OPERATION)


def test_find_value_type_rejects_a_datetime_with_a_time_zone() -> None:
	"""
	Check that a datetime with a time zone raises TimeZoneMismatchError, an Array holding none.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(TimeZoneMismatchError):
		find_value_type(UTC_DATETIME)


def test_find_value_type_reads_a_time_as_time() -> None:
	"""
	Check the type of a Python time of day.

	.. versionadded:: 0.1.0
	"""
	value_type = find_value_type(AFTERNOON)

	assert value_type == Type.TIME


def test_find_value_type_rejects_a_time_with_a_zone() -> None:
	"""
	Check that a time of day with a time zone raises TimeZoneMismatchError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(TimeZoneMismatchError):
		find_value_type(ZONED_AFTERNOON)

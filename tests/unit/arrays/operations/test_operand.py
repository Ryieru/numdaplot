"""
Unit tests of the operands an Array can be combined with.

.. versionadded:: 0.1.0
"""

from datetime import date, time, timedelta

import numpy

from numdaplot.arrays.operations.operand import (
	convert_time_value,
	find_array_operand_type,
	find_operand_type,
	find_operand_type_names,
)
from numdaplot.types.type import Type

SINGLE_VALUES = [True, 3, 2.5, "Paris", date(2026, 1, 31), timedelta(hours=1)]
REJECTED_OPERANDS = [[1, 2], (1, 2), numpy.array([1, 2]), None]
DECIMAL_VALUES = numpy.array([1.5])
TEXT_VALUE = "euros"
EXPECTED_TYPE_NAMES = ["FLOAT64", "TEXT"]
DAY = date(2026, 1, 31)
EXPECTED_DAY = numpy.datetime64("2026-01-31")
ONE_HOUR = timedelta(hours=1)
NUMBER = 3
AFTERNOON = time(15, 35)
AFTERNOON_MICROSECONDS = numpy.timedelta64(56100000000, "us")
LARGE_NUMBER = 300
SMALL_INTEGERS = numpy.array([1], dtype=numpy.int8)


def test_find_operand_type_reads_the_type_of_array_values() -> None:
	"""
	Check that numpy values give their numdaplot type.

	.. versionadded:: 0.1.0
	"""
	operand_type = find_operand_type(DECIMAL_VALUES)

	assert operand_type == Type.FLOAT64


def test_find_array_operand_type_skips_a_single_value_on_the_left() -> None:
	"""
	Check that a Python number before the Array values gives the type of the Array.

	.. versionadded:: 0.2.0
	"""
	array_type = find_array_operand_type([LARGE_NUMBER, SMALL_INTEGERS])

	assert array_type == Type.INT8


def test_find_operand_type_names_lists_each_type_in_order() -> None:
	"""
	Check the names of the types of an Array and of a text.

	.. versionadded:: 0.1.0
	"""
	type_names = find_operand_type_names([DECIMAL_VALUES, TEXT_VALUE])

	assert type_names == EXPECTED_TYPE_NAMES


def test_convert_time_value_converts_a_date_to_numpy() -> None:
	"""
	Check that a Python date becomes a numpy date.

	.. versionadded:: 0.1.0
	"""
	converted_value = convert_time_value(DAY)

	assert converted_value == EXPECTED_DAY


def test_convert_time_value_converts_a_duration_to_numpy() -> None:
	"""
	Check that a Python duration becomes a numpy duration.

	.. versionadded:: 0.1.0
	"""
	converted_value = convert_time_value(ONE_HOUR)

	assert isinstance(converted_value, numpy.timedelta64)


def test_convert_time_value_keeps_other_values() -> None:
	"""
	Check that a number is returned as it is.

	.. versionadded:: 0.1.0
	"""
	converted_value = convert_time_value(NUMBER)

	assert converted_value == NUMBER


def test_convert_time_value_counts_a_very_long_duration_in_seconds() -> None:
	"""
	Check a duration that microseconds cannot count, which numpy would write as a wrong value.

	.. versionadded:: 0.1.0
	"""
	very_long_duration = timedelta(days=200000000)

	converted_duration = convert_time_value(very_long_duration)

	expected_duration = numpy.timedelta64(200000000, "D")
	assert converted_duration == expected_duration


def test_convert_time_value_keeps_microseconds_of_a_usual_duration() -> None:
	"""
	Check a duration microseconds can count.

	.. versionadded:: 0.1.0
	"""
	usual_duration = timedelta(microseconds=1)

	converted_duration = convert_time_value(usual_duration)

	expected_duration = numpy.timedelta64(1, "us")
	assert converted_duration == expected_duration


def test_convert_time_value_gives_the_microseconds_since_midnight() -> None:
	"""
	Check that a time of day is compared as its time since midnight.

	.. versionadded:: 0.1.0
	"""
	converted_value = convert_time_value(AFTERNOON)

	assert converted_value == AFTERNOON_MICROSECONDS
	assert converted_value.dtype == AFTERNOON_MICROSECONDS.dtype

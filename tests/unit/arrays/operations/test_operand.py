"""
Unit tests of the operands an Array can be combined with.

.. versionadded:: 0.1.0
"""

from datetime import date, timedelta

import numpy
import pytest

from numdaplot.arrays.operations.operand import (
	convert_time_value,
	find_operand_type,
	find_operand_type_names,
	require_single_value,
)
from numdaplot.data_types.type import Type
from numdaplot.errors.unsupported_operand_error import UnsupportedOperandError

SINGLE_VALUES = [True, 3, 2.5, "Paris", date(2026, 1, 31), timedelta(hours=1)]
REJECTED_OPERANDS = [[1, 2], (1, 2), numpy.array([1, 2]), None]
DECIMAL_VALUES = numpy.array([1.5])
TEXT_VALUE = "euros"
EXPECTED_TYPE_NAMES = ["FLOAT64", "TEXT"]
DAY = date(2026, 1, 31)
EXPECTED_DAY = numpy.datetime64("2026-01-31")
ONE_HOUR = timedelta(hours=1)
NUMBER = 3


@pytest.mark.parametrize("value", SINGLE_VALUES)
def test_require_single_value_accepts_each_kind_of_single_value(value: object) -> None:
	"""
	Check that booleans, numbers, texts, dates and durations are accepted.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		A single value.
	"""
	require_single_value(value)


@pytest.mark.parametrize("operand", REJECTED_OPERANDS)
def test_require_single_value_rejects_containers_and_none(operand: object) -> None:
	"""
	Check that lists, tuples, numpy arrays and None are rejected.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operand
		A rejected operand.
	"""
	with pytest.raises(UnsupportedOperandError):
		require_single_value(operand)


def test_find_operand_type_reads_the_type_of_array_values() -> None:
	"""
	Check that numpy values give their numdaplot type.

	.. versionadded:: 0.1.0
	"""
	operand_type = find_operand_type(DECIMAL_VALUES)

	assert operand_type == Type.FLOAT64


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

"""
Values an Array can be combined with.

.. versionadded:: 0.1.0
"""

from datetime import date, time, timedelta
from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.rules.rule_values import ScalarValue
from numdaplot.types.numpy_mapping import from_numpy_dtype
from numdaplot.types.time_of_day import to_time_since_midnight
from numdaplot.types.type import Type
from numdaplot.types.value_type import find_value_type

MICROSECONDS_IN_COUNT = 2**63 - 1
LONGEST_MICROSECOND_DURATION = timedelta(microseconds=MICROSECONDS_IN_COUNT)
ONE_SECOND = timedelta(seconds=1)
SECOND_CODE = "s"
TIME_CODE = "us"

type Operand = NDArray[Any] | ScalarValue
"""The values of an Array, or a single value, on one side of an operation.

.. versionadded:: 0.1.0
"""


def find_operand_type(operand: Operand) -> Type:
	"""
	Return the numdaplot type of the values on one side of an operation.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operand
		The values of an Array, or a single value.

	Returns
	-------
	Type
		The type of the values.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.operand import find_operand_type
	>>> find_operand_type(numpy.array([1.5]))
	<Type.FLOAT64: 10>
	"""
	if isinstance(operand, numpy.ndarray):
		array_type = from_numpy_dtype(operand.dtype)
		return array_type

	value_type = find_value_type(operand)

	return value_type


def find_array_operand_type(operands: list[Operand]) -> Type:
	"""
	Return the type of the first operand holding the values of an Array, which a single value has to fit.

	.. versionadded:: 0.2.0

	Parameters
	----------
	operands
		The values of Arrays, or single values, at least one holding the values of an Array.

	Returns
	-------
	Type
		The type of the values of the first Array among the operands.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.operand import find_array_operand_type
	>>> find_array_operand_type([300, numpy.array([1], dtype=numpy.int8)])
	<Type.INT8: 1>
	"""
	array_operands = [operand for operand in operands if isinstance(operand, numpy.ndarray)]
	first_array_operand = array_operands[0]
	array_type = from_numpy_dtype(first_array_operand.dtype)

	return array_type


def find_operand_type_names(operands: list[Operand]) -> list[str]:
	"""
	Return the names of the numdaplot types of several operands, as shown in error messages.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operands
		The values of Arrays, or single values.

	Returns
	-------
	list[str]
		The name of the type of each operand, in order.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.operand import find_operand_type_names
	>>> find_operand_type_names([numpy.array([1]), "euros"])
	['INT64', 'TEXT']
	"""
	operand_types = [find_operand_type(operand) for operand in operands]
	type_names = [operand_type.name for operand_type in operand_types]

	return type_names


def convert_time_value(value: ScalarValue) -> Any:
	"""
	Return a single value in the form numpy compares with Array values.

	numpy compares a Python date with its own dates through Python objects, which fails on a missing date.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		A single value.

	Returns
	-------
	Any
		A ``numpy.datetime64`` for a date or a datetime, a ``numpy.timedelta64`` for a duration, in seconds when
		microseconds cannot count it, the time since midnight in microseconds for a time of day, the value itself
		otherwise.

	Examples
	--------
	>>> from datetime import date
	>>> from numdaplot.arrays.operations.operand import convert_time_value
	>>> convert_time_value(date(2026, 1, 31))
	np.datetime64('2026-01-31')
	"""
	if isinstance(value, date):
		moment = numpy.datetime64(value)
		return moment

	if isinstance(value, time):
		since_midnight = to_time_since_midnight(value)
		time_of_day = numpy.timedelta64(since_midnight, TIME_CODE)
		return time_of_day

	if isinstance(value, timedelta):
		is_too_long_for_microseconds = abs(value) > LONGEST_MICROSECOND_DURATION
		if is_too_long_for_microseconds:
			whole_seconds = value // ONE_SECOND
			second_duration = numpy.timedelta64(whole_seconds, SECOND_CODE)
			return second_duration

		duration = numpy.timedelta64(value)
		return duration

	return value

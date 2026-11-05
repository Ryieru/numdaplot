"""
Values an Array can be combined with.

.. versionadded:: 0.1.0
"""

from datetime import date, timedelta
from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.data_types.numpy_mapping import from_numpy_dtype
from numdaplot.data_types.type import Type
from numdaplot.data_types.value_type import find_value_type
from numdaplot.rules.rule_values import ScalarValue

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
		A ``numpy.datetime64`` for a date or a datetime, a ``numpy.timedelta64`` for a duration,
		the value itself otherwise.

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

	if isinstance(value, timedelta):
		duration = numpy.timedelta64(value)
		return duration

	return value

"""
Combination of two operands with an arithmetic or boolean function.

.. versionadded:: 0.1.0
"""

import warnings
from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.operations.operand import Operand, find_operand_type_names
from numdaplot.arrays.operations.time_arithmetic import combine_time_values, involves_time
from numdaplot.errors.broadcast_warning import BroadcastWarning
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.shape_mismatch_error import ShapeMismatchError

PYTHON_OBJECT_KIND = "O"
BROADCAST_MESSAGE = "Shapes {left_dimensions} and {right_dimensions} differ, values are repeated to match."
# The warning points at the user line: check_shapes, combine_values, the Array helper, the operator, the user.
BROADCAST_STACK_LEVEL = 5


def combine_values(left: Operand, right: Operand, function: numpy.ufunc, symbol: str) -> NDArray[Any]:
	"""
	Return the result of a numpy function applied to two operands, value by value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The values of an Array, or a single value.
	right
		The values of an Array, or a single value. At least one side is the values of an Array.
	function
		The numpy function, such as ``numpy.add``.
	symbol
		The operator shown in error messages, such as ``+``.

	Returns
	-------
	NDArray
		The combined values, following the numpy type rules, and the rules of ``combine_time_values`` for
		dates, datetimes and durations.

	Warns
	-----
	BroadcastWarning
		When both sides are Array values of different but compatible shapes.

	Raises
	------
	ShapeMismatchError
		When both sides are Array values whose shapes cannot be combined.
	IncompatibleTypesError
		When the function does not apply to the types of the operands.
	RefusedOperationError, ValueConversionError
		When a time operation is refused, as in ``combine_time_values``.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.combination import combine_values
	>>> combine_values(numpy.array([1, 2]), 10, numpy.multiply, "*")
	array([10, 20])
	"""
	check_shapes(left, right)
	has_time = involves_time(left, right)
	if has_time:
		time_values = combine_time_values(left, right, function, symbol)
		return time_values

	operands = list[Operand]([left, right])
	try:
		combined_values = function(left, right)
	except TypeError as error:
		type_names = find_operand_type_names(operands)
		raise IncompatibleTypesError(symbol, type_names) from error

	if combined_values.dtype.kind == PYTHON_OBJECT_KIND:
		type_names = find_operand_type_names(operands)
		raise IncompatibleTypesError(symbol, type_names)

	return combined_values


def check_shapes(left: Operand, right: Operand) -> None:
	"""
	Check that two operands can be combined, and warn when an Array is stretched to match the other.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The values of an Array, or a single value.
	right
		The values of an Array, or a single value.

	Warns
	-----
	BroadcastWarning
		When both sides are Array values of different but compatible shapes.

	Raises
	------
	ShapeMismatchError
		When both sides are Array values whose shapes cannot be combined.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.operations.combination import check_shapes
	>>> try:
	... 	check_shapes(numpy.array([1, 2]), numpy.array([1, 2, 3]))
	... except ndp.ShapeMismatchError as error:
	... 	print(error)
	Expected matching shapes, got (2,) and (3,).
	"""
	if not isinstance(left, numpy.ndarray):
		return

	if not isinstance(right, numpy.ndarray):
		return

	if left.shape == right.shape:
		return

	try:
		numpy.broadcast_shapes(left.shape, right.shape)
	except ValueError as error:
		raise ShapeMismatchError(left.shape, right.shape) from error

	message = BROADCAST_MESSAGE.format(left_dimensions=left.shape, right_dimensions=right.shape)
	warnings.warn(message, BroadcastWarning, stacklevel=BROADCAST_STACK_LEVEL)

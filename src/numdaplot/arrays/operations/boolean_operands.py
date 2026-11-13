"""
Check that the operands of a boolean operator are booleans.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.operations.operand import Operand, find_operand_type, find_operand_type_names
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.types.type import Type


def require_booleans(operands: list[Operand], symbol: str) -> None:
	"""
	Check that every operand of a boolean operator holds booleans.

	``&``, ``|`` and ``~`` combine the masks returned by ``check``. On integers, numpy would
	combine their bits instead, which is refused.

	.. versionadded:: 0.1.0

	Parameters
	----------
	operands
		The values of Arrays, or single values.
	symbol
		The operator shown in error messages, such as ``"&"``.

	Raises
	------
	IncompatibleTypesError
		When an operand is not a boolean.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.operations.boolean_operands import require_booleans
	>>> try:
	... 	require_booleans([numpy.array([True]), 2], "|")
	... except ndp.IncompatibleTypesError as error:
	... 	print(error)
	Cannot apply | to BOOL and INT64.
	"""
	for operand in operands:
		operand_type = find_operand_type(operand)
		if operand_type != Type.BOOL:
			type_names = find_operand_type_names(operands)
			raise IncompatibleTypesError(symbol, type_names)

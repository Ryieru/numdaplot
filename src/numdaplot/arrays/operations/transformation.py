"""
Transformation of each value of an Array with a numpy function of one operand.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.operations.operand import find_operand_type_names
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError


def transform_values(values: NDArray[Any], function: numpy.ufunc, name: str) -> NDArray[Any]:
	"""
	Return the result of a numpy function applied to each value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	function
		The numpy function, such as ``numpy.negative``.
	name
		The operator or function name shown in error messages, such as ``-``.

	Returns
	-------
	NDArray
		The transformed values.

	Raises
	------
	IncompatibleTypesError
		When the function does not apply to the type of the values.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.transformation import transform_values
	>>> transform_values(numpy.array([1, -2]), numpy.negative, "-")
	array([-1,  2])
	"""
	try:
		transformed_values = function(values)
	except TypeError as error:
		type_names = find_operand_type_names([values])
		raise IncompatibleTypesError(name, type_names) from error

	return transformed_values

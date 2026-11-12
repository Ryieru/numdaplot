"""
Application of a math function to each value of an Array.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.math_functions.absolute import Absolute
from numdaplot.arrays.math_functions.cosine import Cosine
from numdaplot.arrays.math_functions.exponential import Exponential
from numdaplot.arrays.math_functions.logarithm import Logarithm
from numdaplot.arrays.math_functions.math_function import MathFunction
from numdaplot.arrays.math_functions.round import Round
from numdaplot.arrays.math_functions.sine import Sine
from numdaplot.arrays.math_functions.square_root import SquareRoot
from numdaplot.arrays.operations.float_errors import FloatErrorWarnings
from numdaplot.arrays.operations.integer_rules import require_absolute_fits
from numdaplot.arrays.operations.type_requirements import require_family
from numdaplot.data_types.number_types import INTEGER_TYPES
from numdaplot.data_types.numpy_mapping import from_numpy_dtype
from numdaplot.data_types.value_family import ValueFamily
from numdaplot.errors.out_of_domain_error import OutOfDomainError
from numdaplot.errors.refused_operation_error import RefusedOperationError

NUMBER_FAMILIES = frozenset({ValueFamily.NUMBER})
DOMAIN_LIMIT = 0
LOGARITHM_FUNCTIONS = {
	2.0: numpy.log2,
	10.0: numpy.log10,
}
UNKNOWN_FUNCTION_OPERATION = "The math function {function_name}"
UNKNOWN_FUNCTION_ALTERNATIVE = "a math function of numdaplot"
DECIMAL_FUNCTIONS = (SquareRoot, Logarithm, Exponential, Sine, Cosine)
DECIMAL_DTYPE = numpy.dtype(numpy.float64)


def apply_math_function(values: NDArray[Any], function: MathFunction) -> NDArray[Any]:
	"""
	Return the result of a math function applied to each value.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		The functions giving decimals give ``FLOAT64`` for integers of any size.

	Parameters
	----------
	values
		The values of a number Array.
	function
		Any math function of numdaplot.

	Returns
	-------
	NDArray
		The transformed values. Missing values stay missing. The functions giving decimals give ``FLOAT64`` for
		integers of any size, and keep ``FLOAT32``; ``Absolute`` and ``Round`` keep the type of the values.

	Raises
	------
	IncompatibleTypesError
		When the values are not numbers.
	OutOfDomainError
		When a value is outside the domain of the function.
	RefusedOperationError
		When the function is not a math function of numdaplot.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.math_function_values import apply_math_function
	>>> apply_math_function(numpy.array([1, 100]), ndp.Logarithm(base=10))
	array([0., 2.])
	"""
	function_class = type(function)
	function_name = function_class.__name__
	require_family(values, NUMBER_FAMILIES, function_name)
	gives_decimals = isinstance(function, DECIMAL_FUNCTIONS)
	calculated_values = find_decimal_values(values) if gives_decimals else values

	with FloatErrorWarnings(function_name):
		match function:
			case SquareRoot():
				require_domain(values, numpy.less, function_name)
				transformed_values = numpy.sqrt(calculated_values)
			case Logarithm():
				require_domain(values, numpy.less_equal, function_name)
				transformed_values = compute_logarithm(calculated_values, function)
			case Exponential():
				transformed_values = numpy.exp(calculated_values)
			case Absolute():
				require_absolute_fits(values, function_name)
				transformed_values = numpy.absolute(values)
			case Round():
				transformed_values = numpy.round(values, function.decimals)
			case Sine():
				transformed_values = numpy.sin(calculated_values)
			case Cosine():
				transformed_values = numpy.cos(calculated_values)
			case _:
				operation = UNKNOWN_FUNCTION_OPERATION.format(function_name=function_name)
				raise RefusedOperationError(operation, UNKNOWN_FUNCTION_ALTERNATIVE)

		return transformed_values


def find_decimal_values(values: NDArray[Any]) -> NDArray[Any]:
	"""
	Return the values a function giving decimals is computed on: integers as ``FLOAT64``, decimals unchanged.

	numpy would compute small integers in its smallest decimal types, which keep about 3 digits for ``INT8``.

	.. versionadded:: 0.2.0

	Parameters
	----------
	values
		The values of a number Array.

	Returns
	-------
	NDArray
		``FLOAT64`` values for integers of any size, the values themselves for decimals.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.calculation.math_function_values import find_decimal_values
	>>> find_decimal_values(numpy.array([4, 9], dtype=numpy.int8)).dtype
	dtype('float64')
	"""
	values_type = from_numpy_dtype(values.dtype)
	if values_type not in INTEGER_TYPES:
		return values

	decimal_values = values.astype(DECIMAL_DTYPE)

	return decimal_values


def require_domain(values: NDArray[Any], is_outside: numpy.ufunc, function_name: str) -> None:
	"""
	Check that no value is outside the domain of a math function, by comparison with 0.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of a number Array. Missing values are never outside.
	is_outside
		The comparison with 0 telling a value is outside, such as ``numpy.less`` for a square root.
	function_name
		Name of the math function, shown in the error message.

	Raises
	------
	OutOfDomainError
		At the first value outside the domain.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.math_function_values import require_domain
	>>> try:
	... 	require_domain(numpy.array([4, -9]), numpy.less, "SquareRoot")
	... except ndp.OutOfDomainError as error:
	... 	print(error)
	SquareRoot is not defined for -9.
	"""
	outside = is_outside(values, DOMAIN_LIMIT)
	has_outside_value = outside.any()
	if has_outside_value:
		outside_values = values[outside]
		first_outside_value = outside_values[0]
		rejected_value = first_outside_value.item()
		raise OutOfDomainError(function_name, rejected_value)


def compute_logarithm(values: NDArray[Any], logarithm: Logarithm) -> NDArray[Any]:
	"""
	Return the logarithm of each value, in the base of a ``Logarithm``.

	Bases 2 and 10 use their dedicated numpy functions, which give exact results on exact powers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values, all greater than 0 or missing.
	logarithm
		The base, natural when ``None``.

	Returns
	-------
	NDArray
		The logarithm of each value.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.calculation.math_function_values import compute_logarithm
	>>> compute_logarithm(numpy.array([8]), ndp.Logarithm(base=2))
	array([3.])
	"""
	natural_logarithms = numpy.log(values)
	base = logarithm.base
	if base is None:
		return natural_logarithms

	if base in LOGARITHM_FUNCTIONS:
		dedicated_function = LOGARITHM_FUNCTIONS[base]
		dedicated_logarithms = dedicated_function(values)
		return dedicated_logarithms

	base_logarithm = numpy.log(base)
	logarithms = natural_logarithms / base_logarithm

	return logarithms

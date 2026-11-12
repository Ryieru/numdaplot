"""
Unit tests of apply_math_function, require_domain and compute_logarithm.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

from numdaplot.arrays.calculation.math_function_values import (
	apply_math_function,
	compute_logarithm,
	find_decimal_values,
	require_domain,
)
from numdaplot.arrays.math_functions.absolute import Absolute
from numdaplot.arrays.math_functions.cosine import Cosine
from numdaplot.arrays.math_functions.exponential import Exponential
from numdaplot.arrays.math_functions.logarithm import Logarithm
from numdaplot.arrays.math_functions.math_function import MathFunction
from numdaplot.arrays.math_functions.round import Round
from numdaplot.arrays.math_functions.sine import Sine
from numdaplot.arrays.math_functions.square_root import SquareRoot
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.out_of_domain_error import OutOfDomainError
from numdaplot.errors.refused_operation_error import RefusedOperationError

TEXT_DTYPE = "T"
FUNCTIONS = [
	(SquareRoot(), [0, 4, 9], [0.0, 2.0, 3.0]),
	(Exponential(), [0], [1.0]),
	(Absolute(), [-3, 3], [3, 3]),
	(Round(decimals=0), [2.5, 3.5], [2.0, 4.0]),
	(Round(decimals=-2), [1234], [1200]),
	(Sine(), [0], [0.0]),
	(Cosine(), [0], [1.0]),
	(Logarithm(base=10), [1, 1000], [0.0, 3.0]),
]
NEGATIVE_VALUES = [4, -9]
DECIMAL_FUNCTIONS = [SquareRoot(), Exponential(), Logarithm(), Sine(), Cosine()]
TYPE_KEEPING_FUNCTIONS = [Absolute(), Round()]
INTEGER_DTYPES = [numpy.int8, numpy.uint8, numpy.int16, numpy.uint16, numpy.int32, numpy.int64]
DECIMAL_DTYPE = numpy.dtype(numpy.float64)
SMALL_DECIMAL_DTYPE = numpy.dtype(numpy.float32)
SMALL_INTEGERS = numpy.array([1, 4], dtype=numpy.int8)
SMALL_DECIMALS = numpy.array([1.0, 4.0], dtype=numpy.float32)
REJECTED_VALUE = -9
ZERO_VALUES = [0.0]
MISSING_DECIMALS = [1.0, numpy.nan]
EXPECTED_MISSING_MASK = [False, True]
TEXTS = ["a"]
NATURAL_LOGARITHM = Logarithm()
EULER_POWERS = [1.0, numpy.e]
EXPECTED_NATURAL_LOGARITHMS = [0.0, 1.0]
BINARY_LOGARITHM = Logarithm(base=2)
POWERS_OF_TWO = [8]
EXPECTED_BINARY_LOGARITHMS = [3.0]
TERNARY_LOGARITHM = Logarithm(base=3)
POWERS_OF_THREE = [9]
EXPECTED_TERNARY_LOGARITHMS = [2.0]
SQUARE_ROOT_NAME = "SquareRoot"


class UnknownFunction(MathFunction):
	"""
	A math function numdaplot does not know.

	.. versionadded:: 0.1.0
	"""


@pytest.mark.parametrize(("function", "values", "expected_values"), FUNCTIONS)
def test_apply_math_function_applies_each_function(
	function: MathFunction, values: list[float], expected_values: list[float]
) -> None:
	"""
	Check the result of each math function.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function
		A math function.
	values
		The values it receives.
	expected_values
		Its results.
	"""
	numpy_values = numpy.array(values)

	transformed_values = apply_math_function(numpy_values, function)

	is_close = numpy.allclose(transformed_values, expected_values)
	assert is_close


def test_apply_math_function_rejects_the_square_root_of_a_negative_value() -> None:
	"""
	Check that a negative value raises OutOfDomainError naming it.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(NEGATIVE_VALUES)

	with pytest.raises(OutOfDomainError) as error_information:
		apply_math_function(values, SquareRoot())

	assert error_information.value.value == REJECTED_VALUE


def test_apply_math_function_rejects_the_logarithm_of_zero() -> None:
	"""
	Check that 0 is outside the domain of a logarithm.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(ZERO_VALUES)

	with pytest.raises(OutOfDomainError):
		apply_math_function(values, NATURAL_LOGARITHM)


def test_apply_math_function_keeps_missing_values_missing() -> None:
	"""
	Check that NaN goes through without error and stays NaN.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(MISSING_DECIMALS)

	transformed_values = apply_math_function(values, SquareRoot())

	missing = numpy.isnan(transformed_values)
	missing_list = missing.tolist()
	assert missing_list == EXPECTED_MISSING_MASK


def test_apply_math_function_rejects_texts() -> None:
	"""
	Check that math functions only apply to numbers.

	.. versionadded:: 0.1.0
	"""
	texts = numpy.array(TEXTS, dtype=TEXT_DTYPE)

	with pytest.raises(IncompatibleTypesError):
		apply_math_function(texts, Absolute())


def test_apply_math_function_refuses_an_unknown_function() -> None:
	"""
	Check that a math function outside numdaplot raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(ZERO_VALUES)

	with pytest.raises(RefusedOperationError):
		apply_math_function(values, UnknownFunction())


def test_require_domain_ignores_missing_values() -> None:
	"""
	Check that NaN is never outside a domain.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(MISSING_DECIMALS)

	require_domain(values, numpy.less, SQUARE_ROOT_NAME)


def test_compute_logarithm_is_natural_without_base() -> None:
	"""
	Check that the logarithm of e is 1 without base.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(EULER_POWERS)

	logarithms = compute_logarithm(values, NATURAL_LOGARITHM)

	is_close = numpy.allclose(logarithms, EXPECTED_NATURAL_LOGARITHMS)
	assert is_close


def test_compute_logarithm_is_exact_in_base_two() -> None:
	"""
	Check that the logarithm of 8 in base 2 is exactly 3.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(POWERS_OF_TWO)

	logarithms = compute_logarithm(values, BINARY_LOGARITHM)

	logarithm_list = logarithms.tolist()
	assert logarithm_list == EXPECTED_BINARY_LOGARITHMS


def test_compute_logarithm_divides_by_the_logarithm_of_any_other_base() -> None:
	"""
	Check that the logarithm of 9 in base 3 is 2.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(POWERS_OF_THREE)

	logarithms = compute_logarithm(values, TERNARY_LOGARITHM)

	is_close = numpy.allclose(logarithms, EXPECTED_TERNARY_LOGARITHMS)
	assert is_close


@pytest.mark.parametrize("function", DECIMAL_FUNCTIONS)
@pytest.mark.parametrize("integer_dtype", INTEGER_DTYPES)
def test_apply_math_function_gives_decimals_of_64_bits_for_integers(
	function: MathFunction, integer_dtype: type[numpy.integer]
) -> None:
	"""
	Check that a function giving decimals gives FLOAT64 for integers of any size, never the small types of numpy.

	.. versionadded:: 0.2.0

	Parameters
	----------
	function
		A math function giving decimals.
	integer_dtype
		A numpy integer type.
	"""
	values = numpy.array([1, 4], dtype=integer_dtype)

	transformed_values = apply_math_function(values, function)

	assert transformed_values.dtype == DECIMAL_DTYPE


@pytest.mark.parametrize("function", TYPE_KEEPING_FUNCTIONS)
def test_apply_math_function_keeps_the_integer_type_for_absolute_and_round(function: MathFunction) -> None:
	"""
	Check that Absolute and Round keep small integers in their type.

	.. versionadded:: 0.2.0

	Parameters
	----------
	function
		Absolute or Round.
	"""
	transformed_values = apply_math_function(SMALL_INTEGERS, function)

	assert transformed_values.dtype == SMALL_INTEGERS.dtype


def test_find_decimal_values_gives_decimals_of_64_bits_for_integers() -> None:
	"""
	Check that integers are given as FLOAT64.

	.. versionadded:: 0.2.0
	"""
	decimal_values = find_decimal_values(SMALL_INTEGERS)

	assert decimal_values.dtype == DECIMAL_DTYPE


def test_find_decimal_values_keeps_decimals_as_they_are() -> None:
	"""
	Check that FLOAT32 values stay the same values.

	.. versionadded:: 0.2.0
	"""
	decimal_values = find_decimal_values(SMALL_DECIMALS)

	assert decimal_values is SMALL_DECIMALS

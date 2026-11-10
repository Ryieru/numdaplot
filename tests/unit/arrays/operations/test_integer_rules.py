"""
Unit tests of the refusal of integer calculations numpy would write as a wrong number.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

from numdaplot.arrays.operations.integer_rules import (
	do_bounds_fit,
	find_doubtful_estimates,
	require_absolute_fits,
	require_combination_fits,
	require_defined_integers,
	require_exact_values_fit,
	require_opposite_fits,
	require_sum_fits,
)
from numdaplot.errors.integer_overflow_error import IntegerOverflowError
from numdaplot.errors.out_of_domain_error import OutOfDomainError

INTEGERS = numpy.array([1, 2])
DECIMALS = numpy.array([1.0, 2.0])
LARGE_INTEGERS = numpy.array([2**62, 2**62])
CANCELLING_INTEGERS = numpy.array([2**62, -(2**62), 2**62, -(2**62), 1])
EMPTY_INTEGERS = numpy.array([], dtype="int64")
INT8_RESULT = numpy.array([0], dtype="int8")
UINT8_RESULT = numpy.array([0], dtype="uint8")
INT64_RESULT = numpy.array([0])
OPERATION_NAME = "+"


@pytest.mark.parametrize("function", [numpy.floor_divide, numpy.remainder])
def test_require_defined_integers_refuses_a_zero_divisor(function: numpy.ufunc) -> None:
	"""
	Check the refusal of a division by 0 between integers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function
		The division.
	"""
	with pytest.raises(OutOfDomainError):
		require_defined_integers(INTEGERS, 0, function)


def test_require_defined_integers_accepts_a_zero_divisor_of_decimals() -> None:
	"""
	Check that decimals, which can hold the result, are not refused.

	.. versionadded:: 0.1.0
	"""
	require_defined_integers(DECIMALS, 0, numpy.floor_divide)


def test_require_defined_integers_keeps_the_true_division() -> None:
	"""
	Check that a true division, which gives decimals, is not refused.

	.. versionadded:: 0.1.0
	"""
	require_defined_integers(INTEGERS, 0, numpy.true_divide)


def test_require_defined_integers_refuses_a_negative_power() -> None:
	"""
	Check the refusal of a negative power between integers, giving the first negative value.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(OutOfDomainError) as error_info:
		require_defined_integers(INTEGERS, numpy.array([1, -3]), numpy.power)

	assert error_info.value.value == -3


def test_require_defined_integers_accepts_a_negative_power_of_decimals() -> None:
	"""
	Check that a decimal base accepts a negative power.

	.. versionadded:: 0.1.0
	"""
	require_defined_integers(DECIMALS, -1, numpy.power)


def test_require_combination_fits_refuses_a_wrapped_product() -> None:
	"""
	Check the refusal of a product above the limit.

	.. versionadded:: 0.1.0
	"""
	wrapped_result = numpy.multiply(LARGE_INTEGERS, 4)

	with pytest.raises(IntegerOverflowError):
		require_combination_fits([LARGE_INTEGERS, 4], numpy.multiply, wrapped_result, "*")


def test_require_combination_fits_ignores_a_decimal_result() -> None:
	"""
	Check that decimal results are not checked.

	.. versionadded:: 0.1.0
	"""
	require_combination_fits([DECIMALS, 2.0], numpy.multiply, DECIMALS, "*")


def test_require_combination_fits_ignores_a_function_that_cannot_overflow() -> None:
	"""
	Check that a remainder is not checked.

	.. versionadded:: 0.1.0
	"""
	require_combination_fits([LARGE_INTEGERS, 3], numpy.remainder, LARGE_INTEGERS, "%")


def test_require_sum_fits_refuses_a_wrapped_sum() -> None:
	"""
	Check the refusal of a sum above the limit.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(IntegerOverflowError):
		require_sum_fits(LARGE_INTEGERS, None, INT64_RESULT, OPERATION_NAME)


def test_require_sum_fits_ignores_decimals() -> None:
	"""
	Check that a decimal sum is not checked.

	.. versionadded:: 0.1.0
	"""
	require_sum_fits(DECIMALS, None, DECIMALS, OPERATION_NAME)


def test_require_sum_fits_accepts_an_empty_sum() -> None:
	"""
	Check that a sum without values is accepted.

	.. versionadded:: 0.1.0
	"""
	require_sum_fits(EMPTY_INTEGERS, None, INT64_RESULT, OPERATION_NAME)


def test_require_sum_fits_accepts_large_values_cancelling_each_other() -> None:
	"""
	Check that large values whose sum stays far from the limit are accepted without exact calculation.

	.. versionadded:: 0.1.0
	"""
	values_sum = CANCELLING_INTEGERS.sum()
	result = numpy.array(values_sum)

	require_sum_fits(CANCELLING_INTEGERS, None, result, OPERATION_NAME)


def test_find_doubtful_estimates_keeps_only_values_near_the_limit() -> None:
	"""
	Check which estimates need an exact calculation.

	.. versionadded:: 0.1.0
	"""
	estimates = numpy.array([1.0, 100.0])

	doubtful = find_doubtful_estimates(estimates, INT8_RESULT, OPERATION_NAME)

	assert doubtful.tolist() == [False, True]


def test_find_doubtful_estimates_marks_values_below_an_unsigned_type() -> None:
	"""
	Check that a negative estimate is doubtful for an unsigned type.

	.. versionadded:: 0.1.0
	"""
	estimates = numpy.array([-1.0])

	doubtful = find_doubtful_estimates(estimates, UINT8_RESULT, OPERATION_NAME)

	assert doubtful.tolist() == [True]


def test_find_doubtful_estimates_refuses_an_estimate_far_above_the_limit() -> None:
	"""
	Check that an infinite estimate is refused without any exact calculation.

	.. versionadded:: 0.1.0
	"""
	estimates = numpy.array([numpy.inf])

	with pytest.raises(IntegerOverflowError):
		find_doubtful_estimates(estimates, INT64_RESULT, OPERATION_NAME)


def test_require_exact_values_fit_accepts_the_limits() -> None:
	"""
	Check that the limits of the type are accepted.

	.. versionadded:: 0.1.0
	"""
	exact_values = numpy.array([-128, 127], dtype=object)

	require_exact_values_fit(exact_values, INT8_RESULT, OPERATION_NAME)


@pytest.mark.parametrize("value", [-129, 128])
def test_require_exact_values_fit_refuses_a_value_outside_the_limits(value: int) -> None:
	"""
	Check the refusal just outside the limits of the type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		The value.
	"""
	exact_values = numpy.array([value], dtype=object)

	with pytest.raises(IntegerOverflowError):
		require_exact_values_fit(exact_values, INT8_RESULT, OPERATION_NAME)


def test_require_absolute_fits_refuses_the_lowest_integer() -> None:
	"""
	Check that the lowest integer, whose absolute value does not fit, is refused.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([-128], dtype="int8")

	with pytest.raises(IntegerOverflowError):
		require_absolute_fits(values, OPERATION_NAME)


def test_require_absolute_fits_accepts_unsigned_integers() -> None:
	"""
	Check that unsigned integers are their own absolute value.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([255], dtype="uint8")

	require_absolute_fits(values, OPERATION_NAME)


def test_require_opposite_fits_refuses_a_positive_unsigned_integer() -> None:
	"""
	Check that a positive unsigned integer has no opposite.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([1], dtype="uint8")

	with pytest.raises(IntegerOverflowError):
		require_opposite_fits(values, OPERATION_NAME)


def test_require_opposite_fits_refuses_the_lowest_integer() -> None:
	"""
	Check that the lowest integer has no opposite.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([-128], dtype="int8")

	with pytest.raises(IntegerOverflowError):
		require_opposite_fits(values, OPERATION_NAME)


def test_require_opposite_fits_accepts_regular_values() -> None:
	"""
	Check that regular integers and decimals are accepted.

	.. versionadded:: 0.1.0
	"""
	require_opposite_fits(INTEGERS, OPERATION_NAME)
	require_opposite_fits(DECIMALS, OPERATION_NAME)


def test_do_bounds_fit_accepts_the_limits_of_the_type() -> None:
	"""
	Check that bounds equal to the limits fit.

	.. versionadded:: 0.1.0
	"""
	bounds_fit = do_bounds_fit((-128, 127), INT8_RESULT)

	assert bounds_fit


@pytest.mark.parametrize("bounds", [(-129, 0), (0, 128)])
def test_do_bounds_fit_refuses_bounds_outside_the_limits(bounds: tuple[int, int]) -> None:
	"""
	Check that bounds just outside the limits do not fit.

	.. versionadded:: 0.1.0

	Parameters
	----------
	bounds
		The bounds.
	"""
	bounds_fit = do_bounds_fit(bounds, INT8_RESULT)

	assert not bounds_fit


def test_require_combination_fits_accepts_empty_values() -> None:
	"""
	Check that empty values, which have no bounds, are accepted.

	.. versionadded:: 0.1.0
	"""
	empty_values = numpy.array([], dtype="int64")

	require_combination_fits([empty_values, 2], numpy.add, empty_values, OPERATION_NAME)

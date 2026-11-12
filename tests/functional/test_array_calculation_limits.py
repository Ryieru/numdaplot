"""
Functional tests of the calculations reaching the limits of their type.

.. versionadded:: 0.1.0
"""

import warnings
from datetime import timedelta
from typing import Any

import numpy
import pytest

import numdaplot as ndp

HUGE_DECIMAL = 1e308
LARGE_INTEGER = 2**62
HIGHEST_INTEGER = 2**63 - 1
HIGHEST_INT8 = 127
UNDEFINED_MESSAGE = "The operation / has values without a defined result, such as 0 / 0: they became NaN."
ZERO_DIVISION_MESSAGE = "The operation / divides by zero: these values became inf."
TOO_LARGE_MESSAGE = "The operation * has values too large for their type: they became inf."
FLOOR_DIVISION_MESSAGE = "Floor division is not defined for 0 between integers. Convert the values to FLOAT64 first."
REMAINDER_MESSAGE = "Remainder is not defined for 0 between integers. Convert the values to FLOAT64 first."
POWER_MESSAGE = "Power is not defined for -1 between integers. Convert the values to FLOAT64 first."
OVERFLOW_MESSAGE = "The operation {operation} gives values outside the range of {type_name}, {range_and_advice}"
RANGE_AND_ADVICE_BY_TYPE = {
	"INT64": (
		"from -9223372036854775808 to 9223372036854775807. Convert the values to FLOAT64 first, which keeps about 16 "
		"digits."
	),
	"INT8": "from -128 to 127. Convert the values to INT64 first.",
	"UINT8": "from 0 to 255. Convert the values to INT64 first.",
}


def test_zero_divided_by_zero_warns_and_gives_nan() -> None:
	"""
	Check the warning of 0 / 0 on decimals, and the values of the result.

	.. versionadded:: 0.1.0
	"""
	distances = ndp.Array.from_list([0.0, 3.0])
	hours = ndp.Array.from_list([0.0, 2.0])

	with pytest.warns(ndp.CalculationWarning) as caught_warnings:
		speeds = distances / hours

	message = str(caught_warnings[0].message)
	missing = speeds.check(ndp.IsMissing())
	missing_list = missing.to_list()
	assert message == UNDEFINED_MESSAGE
	assert missing_list == [True, False]


def test_a_calculation_warning_points_at_the_calling_line() -> None:
	"""
	Check that the warning gives this file, and no raw numpy warning is left.

	.. versionadded:: 0.1.0
	"""
	zeros = ndp.Array.from_list([0.0])

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		_ = zeros / zeros

	assert len(caught_warnings) == 1
	assert caught_warnings[0].category is ndp.CalculationWarning
	assert caught_warnings[0].filename == __file__


@pytest.mark.parametrize(
	("left", "right", "expected_message"),
	[
		(1.0, 0.0, ZERO_DIVISION_MESSAGE),
		(1, 0, ZERO_DIVISION_MESSAGE),
	],
)
def test_a_division_by_zero_warns_and_gives_inf(left: float, right: float, expected_message: str) -> None:
	"""
	Check that a true division by zero gives an infinite value, for decimals and integers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The value divided.
	right
		The divisor.
	expected_message
		The message of the warning.
	"""
	dividends = ndp.Array.from_list([left])
	divisors = ndp.Array.from_list([right])

	with pytest.warns(ndp.CalculationWarning) as caught_warnings:
		quotients = dividends / divisors

	message = str(caught_warnings[0].message)
	quotient = quotients.to_value()
	assert message == expected_message
	assert quotient == numpy.inf


def test_a_decimal_too_large_warns_and_gives_inf() -> None:
	"""
	Check the warning of a decimal too large for its type.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([HUGE_DECIMAL])

	with pytest.warns(ndp.CalculationWarning) as caught_warnings:
		products = values * 10.0

	message = str(caught_warnings[0].message)
	product = products.to_value()
	assert message == TOO_LARGE_MESSAGE
	assert product == numpy.inf


@pytest.mark.parametrize("statistic", [ndp.Sum(), ndp.Mean(), ndp.StandardDeviation()])
def test_a_statistic_too_large_gives_a_calculation_warning(statistic: ndp.Statistic) -> None:
	"""
	Check that statistics give the warning of numdaplot, named after them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	statistic
		The statistic.
	"""
	values = ndp.Array.from_list([HUGE_DECIMAL, HUGE_DECIMAL])
	statistic_name = type(statistic).__name__

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		values.compute(statistic)

	categories = {caught_warning.category for caught_warning in caught_warnings}
	messages = [str(caught_warning.message) for caught_warning in caught_warnings]
	assert categories == {ndp.CalculationWarning}
	assert statistic_name in messages[0]


def test_exponential_too_large_gives_a_calculation_warning() -> None:
	"""
	Check that a math function gives the warning of numdaplot, named after it.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([HUGE_DECIMAL])

	with pytest.warns(ndp.CalculationWarning, match="Exponential"):
		values.apply(ndp.Exponential())


def test_a_calculation_warning_can_be_silenced() -> None:
	"""
	Check that the standard warnings filter applies.

	.. versionadded:: 0.1.0
	"""
	zeros = ndp.Array.from_list([0.0])

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		warnings.simplefilter("ignore", category=ndp.CalculationWarning)
		_ = zeros / zeros

	assert caught_warnings == []


def test_a_regular_calculation_gives_no_warning() -> None:
	"""
	Check that missing values alone do not warn.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([None, 1.0])

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		_ = values / 2.0

	assert caught_warnings == []


@pytest.mark.parametrize(
	("calculate", "expected_message"),
	[
		(lambda: ndp.Array.from_list([1, 2]) // ndp.Array.from_list([0, 1]), FLOOR_DIVISION_MESSAGE),
		(lambda: ndp.Array.from_list([1, 2]) // 0, FLOOR_DIVISION_MESSAGE),
		(lambda: ndp.Array.from_list([1, 2]) % ndp.Array.from_list([0, 1]), REMAINDER_MESSAGE),
		(lambda: ndp.Array.from_list([1, 2]) ** -1, POWER_MESSAGE),
		(lambda: 2 ** ndp.Array.from_list([-1, 2]), POWER_MESSAGE),
	],
)
def test_integers_refuse_a_result_they_cannot_hold(calculate: Any, expected_message: str) -> None:
	"""
	Check the refusal of a division by 0 and of a negative power between integers.

	.. versionadded:: 0.1.0

	Parameters
	----------
	calculate
		The calculation.
	expected_message
		The message of the error.
	"""
	with pytest.raises(ndp.OutOfDomainError) as error_info:
		calculate()

	error_text = str(error_info.value)
	assert error_text == expected_message


def test_reflected_integer_division_by_zero_is_refused() -> None:
	"""
	Check the refusal when the Array holding 0 is on the right of the operator.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([0, 1])

	with pytest.raises(ndp.OutOfDomainError):
		_ = 5 // values


def test_the_advice_for_integers_works() -> None:
	"""
	Check that FLOAT64 values, as the messages advise, accept the same calculations.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([1, 2], dtype=ndp.Type.FLOAT64)

	powers = values**-1

	python_values = powers.to_list()
	assert python_values == [1.0, 0.5]


@pytest.mark.parametrize(
	("calculate", "operation", "type_name"),
	[
		(lambda: ndp.Array.from_list([LARGE_INTEGER]) * 4, "*", "INT64"),
		(lambda: ndp.Array.from_list([HIGHEST_INTEGER]) + 1, "+", "INT64"),
		(lambda: ndp.Array.from_list([-HIGHEST_INTEGER]) - 2, "-", "INT64"),
		(lambda: ndp.Array.from_list([2]) ** 64, "**", "INT64"),
		(lambda: ndp.Array.from_list([3]) ** 10**18, "**", "INT64"),
		(lambda: 2 ** ndp.Array.from_list([64]), "**", "INT64"),
		(lambda: ndp.Array.from_list([HIGHEST_INT8], dtype=ndp.Type.INT8) + 1, "+", "INT8"),
		(lambda: ndp.Array.from_list([1], dtype=ndp.Type.INT8) * 1000, "*", "INT8"),
		(lambda: 1000 * ndp.Array.from_list([1], dtype=ndp.Type.INT8), "*", "INT8"),
		(lambda: ndp.Array.from_list([1], dtype=ndp.Type.UINT8) - 2, "-", "UINT8"),
		(lambda: ndp.Array.from_list([1, 2]) * 2**64, "*", "INT64"),
		(lambda: ndp.Array.from_list([-(2**63)]) // -1, "//", "INT64"),
		(lambda: -ndp.Array.from_list([-(2**63)]), "-", "INT64"),
		(lambda: -ndp.Array.from_list([1], dtype=ndp.Type.UINT8), "-", "UINT8"),
		(lambda: ndp.Array.from_list([-(2**63)]).apply(ndp.Absolute()), "Absolute", "INT64"),
	],
)
def test_integers_refuse_a_result_outside_their_range(calculate: Any, operation: str, type_name: str) -> None:
	"""
	Check the refusal of every integer result that numpy would wrap around.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Checks the range of the type and the advice in the message, and a number written before the Array.

	Parameters
	----------
	calculate
		The calculation.
	operation
		The expected operation in the message.
	type_name
		The expected type in the message.
	"""
	range_and_advice = RANGE_AND_ADVICE_BY_TYPE[type_name]
	expected_message = OVERFLOW_MESSAGE.format(
		operation=operation, type_name=type_name, range_and_advice=range_and_advice
	)

	with pytest.raises(ndp.IntegerOverflowError) as error_info:
		calculate()

	error_text = str(error_info.value)
	assert error_text == expected_message


@pytest.mark.parametrize(
	("calculate", "expected_value"),
	[
		(lambda: ndp.Array.from_list([HIGHEST_INTEGER - 1]) + 1, HIGHEST_INTEGER),
		(lambda: ndp.Array.from_list([LARGE_INTEGER]) * 1, LARGE_INTEGER),
		(lambda: ndp.Array.from_list([2]) ** 62, LARGE_INTEGER),
		(lambda: ndp.Array.from_list([HIGHEST_INT8 - 1], dtype=ndp.Type.INT8) + 1, HIGHEST_INT8),
		(lambda: ndp.Array.from_list([2], dtype=ndp.Type.UINT8) - 2, 0),
	],
)
def test_integers_at_their_limit_stay_exact(calculate: Any, expected_value: int) -> None:
	"""
	Check that a result close to the limit of its type is neither refused nor approximated.

	.. versionadded:: 0.1.0

	Parameters
	----------
	calculate
		The calculation.
	expected_value
		Its exact result.
	"""
	result = calculate()

	result_value = result.to_value()
	assert result_value == expected_value


def test_a_refused_integer_result_gives_no_warning() -> None:
	"""
	Check that the error is the only signal of the lowest integer divided by -1.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([-(2**63)])

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		with pytest.raises(ndp.IntegerOverflowError):
			_ = values // -1

	assert caught_warnings == []


def test_a_sum_of_integers_too_large_is_refused() -> None:
	"""
	Check the refusal of a sum that numpy would wrap around.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([LARGE_INTEGER, LARGE_INTEGER])

	with pytest.raises(ndp.IntegerOverflowError):
		values.compute(ndp.Sum())


def test_a_sum_of_integers_along_an_axis_too_large_is_refused() -> None:
	"""
	Check the refusal when a single row overflows.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([[LARGE_INTEGER, LARGE_INTEGER], [1, 2]])

	with pytest.raises(ndp.IntegerOverflowError):
		values.compute(ndp.Sum(), axis=ndp.Axis.EACH_ROW)


def test_a_sum_coming_back_under_the_limit_stays_exact() -> None:
	"""
	Check that only the final sum counts, not the running total.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([HIGHEST_INTEGER, 1, -2])

	total = values.compute(ndp.Sum())

	total_value = total.to_value()
	assert total_value == HIGHEST_INTEGER - 1


def test_an_aggregated_sum_too_large_is_refused() -> None:
	"""
	Check that the refusal also protects the aggregation of a Table.

	.. versionadded:: 0.1.0
	"""
	values = ndp.Array.from_list([LARGE_INTEGER, LARGE_INTEGER])
	table = ndp.Table.from_arrays({"amount": values})
	total = ndp.Calculation(column="amount", function=ndp.Sum())

	with pytest.raises(ndp.IntegerOverflowError):
		table.aggregate(ndp.Aggregation(calculations=[total]))


def test_the_integer_refusals_are_numdaplot_errors() -> None:
	"""
	Check that a single except clause catches both refusals.

	.. versionadded:: 0.1.0
	"""
	assert issubclass(ndp.IntegerOverflowError, ndp.NumdaplotError)
	assert issubclass(ndp.OutOfDomainError, ndp.NumdaplotError)


def test_a_duration_divided_by_zero_stays_missing() -> None:
	"""
	Check that a duration divided by 0 is missing, without warning.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([timedelta(days=1)])
	divisors = ndp.Array.from_list([0])

	with warnings.catch_warnings(record=True) as caught_warnings:
		warnings.simplefilter("always")
		quotients = durations / divisors

	missing = quotients.check(ndp.IsMissing())
	missing_list = missing.to_list()
	assert missing_list == [True]
	assert caught_warnings == []

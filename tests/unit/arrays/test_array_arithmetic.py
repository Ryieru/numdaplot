"""
Unit tests of ArrayArithmetic and ArrayReflectedArithmetic.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from collections.abc import Callable
from typing import Any

import numpy
import pytest

from numdaplot.arrays.array_arithmetic import ArrayArithmetic
from numdaplot.arrays.array_reflected_arithmetic import ArrayReflectedArithmetic
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError

COMBINE_NAME = "_combine"
COMBINE_REFLECTED_NAME = "_combine_reflected"
OPERAND = 2
VALUES = [1, -2]
EXPECTED_NEGATED_VALUES = [-1, 2]
BOOLEANS = [True]
type BinaryOperator = Callable[[Any, Any], Any]
OPERATORS = list[tuple[BinaryOperator, numpy.ufunc, str]](
	[
		(lambda left, right: left + right, numpy.add, "+"),
		(lambda left, right: left - right, numpy.subtract, "-"),
		(lambda left, right: left * right, numpy.multiply, "*"),
		(lambda left, right: left / right, numpy.true_divide, "/"),
		(lambda left, right: left // right, numpy.floor_divide, "//"),
		(lambda left, right: left % right, numpy.remainder, "%"),
		(lambda left, right: left**right, numpy.power, "**"),
	]
)


class CombinationRecorder:
	"""
	Fake combination recording the numpy function and the symbol it receives.

	.. versionadded:: 0.1.0
	"""

	def __init__(self) -> None:
		"""
		Start without recorded call.

		.. versionadded:: 0.1.0
		"""
		self.calls = list[tuple[object, numpy.ufunc, str]]()

	def combine(self, other: object, function: numpy.ufunc, symbol: str) -> None:
		"""
		Record the call.

		Stored on the Array class as a bound method of the recorder, it receives the arguments
		of the replaced helper without the Array itself.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			The other operand.
		function
			The numpy function.
		symbol
			The operator shown in error messages.
		"""
		call = (other, function, symbol)
		self.calls.append(call)


@pytest.mark.parametrize(("python_operator", "function", "symbol"), OPERATORS)
def test_array_arithmetic_hands_each_operator_to_the_combination(
	monkeypatch: pytest.MonkeyPatch, python_operator: BinaryOperator, function: numpy.ufunc, symbol: str
) -> None:
	"""
	Check that each operator combines with its numpy function and its symbol, the Array on the left.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the combination with a fake recording its calls.
	python_operator
		A function applying the Python operator to two operands.
	function
		The expected numpy function.
	symbol
		The expected symbol.
	"""
	recorder = CombinationRecorder()
	monkeypatch.setattr(ArrayArithmetic, COMBINE_NAME, recorder.combine)
	values = numpy.array(VALUES)
	array = ArrayArithmetic._create(values)

	python_operator(array, OPERAND)

	assert recorder.calls == [(OPERAND, function, symbol)]


@pytest.mark.parametrize(("python_operator", "function", "symbol"), OPERATORS)
def test_array_reflected_arithmetic_hands_each_operator_to_the_reflected_combination(
	monkeypatch: pytest.MonkeyPatch, python_operator: BinaryOperator, function: numpy.ufunc, symbol: str
) -> None:
	"""
	Check that each operator with a single value on the left uses the reflected combination.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the reflected combination with a fake recording its calls.
	python_operator
		A function applying the Python operator to two operands.
	function
		The expected numpy function.
	symbol
		The expected symbol.
	"""
	recorder = CombinationRecorder()
	monkeypatch.setattr(ArrayReflectedArithmetic, COMBINE_REFLECTED_NAME, recorder.combine)
	values = numpy.array(VALUES)
	array = ArrayReflectedArithmetic._create(values)

	python_operator(OPERAND, array)

	assert recorder.calls == [(OPERAND, function, symbol)]


def test_array_arithmetic_negates_each_value() -> None:
	"""
	Check that -array gives the opposite of each value.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(VALUES)
	array = ArrayArithmetic._create(values)

	negated_array = -array

	negated_values = negated_array.to_numpy()
	negated_list = negated_values.tolist()
	assert negated_list == EXPECTED_NEGATED_VALUES


def test_array_arithmetic_rejects_the_opposite_of_booleans() -> None:
	"""
	Check that -array on booleans raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	booleans = numpy.array(BOOLEANS)
	array = ArrayArithmetic._create(booleans)

	with pytest.raises(IncompatibleTypesError):
		_ = -array

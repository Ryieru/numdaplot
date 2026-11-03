"""
Unit tests of ArrayData.

.. versionadded:: 0.1.0
"""

from typing import Any, Self

import numpy
import pytest
from numpy.typing import NDArray

from numdaplot.arrays import array_data
from numdaplot.arrays.array_data import ArrayData
from numdaplot.arrays.operations.operand import Operand
from numdaplot.arrays.shape import Shape
from numdaplot.data_types.type import Type
from numdaplot.errors.unsupported_operand_error import UnsupportedOperandError

GRID = [[1, 2, 3], [4, 5, 6]]
GRID_SHAPE = Shape((2, 3))
DECIMALS = [1.5]
CHANGED_VALUE = 99
FIRST_POSITION = (0, 0)
SINGLE_VALUE = 10
REJECTED_OPERAND = [1, 2]
SUBTRACTION_SYMBOL = "-"
COMBINE_VALUES_NAME = "combine_values"
FAKE_RESULT = numpy.array([7, 7])
EXPECTED_FAKE_RESULT = [7, 7]


class ExposedArrayData(ArrayData):
	"""
	ArrayData giving the tests access to its protected helpers.

	.. versionadded:: 0.1.0
	"""

	def read_operand(self, other: object) -> Operand:
		"""
		Call the protected operand reading.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			An Array or a single value.

		Returns
		-------
		Operand
			What the protected helper returns.
		"""
		operand = self._read_operand(other)

		return operand

	def combine(self, other: object) -> Self:
		"""
		Call the protected combination with this data on the left, as a subtraction.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			An Array or a single value.

		Returns
		-------
		Self
			What the protected helper returns.
		"""
		combined = self._combine(other, numpy.subtract, SUBTRACTION_SYMBOL)

		return combined

	def combine_reflected(self, other: object) -> Self:
		"""
		Call the protected combination with this data on the right, as a subtraction.

		.. versionadded:: 0.1.0

		Parameters
		----------
		other
			A single value.

		Returns
		-------
		Self
			What the protected helper returns.
		"""
		combined = self._combine_reflected(other, numpy.subtract, SUBTRACTION_SYMBOL)

		return combined


class OperandRecorder:
	"""
	Fake combination recording its operands.

	.. versionadded:: 0.1.0
	"""

	def __init__(self) -> None:
		"""
		Start without recorded operands.

		.. versionadded:: 0.1.0
		"""
		self.operands = list[Operand]()

	def combine(self, left: Operand, right: Operand, function: numpy.ufunc, symbol: str) -> NDArray[Any]:
		"""
		Record both operands and return a known result.

		.. versionadded:: 0.1.0

		Parameters
		----------
		left
			The left operand.
		right
			The right operand.
		function
			The numpy function, ignored.
		symbol
			The operator, ignored.

		Returns
		-------
		NDArray
			Always the fake result.
		"""
		self.operands.append(left)
		self.operands.append(right)

		return FAKE_RESULT


def test_array_data_reads_its_shape() -> None:
	"""
	Check that the shape is a Shape of the stored values.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	data = ArrayData(values)

	assert data.shape == GRID_SHAPE


def test_array_data_reads_its_type() -> None:
	"""
	Check that the type is the numdaplot type of the stored values.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(DECIMALS)
	data = ArrayData(values)

	assert data.dtype == Type.FLOAT64


def test_array_data_makes_its_values_read_only() -> None:
	"""
	Check that the stored values cannot be written.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)

	ArrayData(values)

	assert not values.flags.writeable


def test_array_data_gives_an_independent_numpy_copy() -> None:
	"""
	Check that changing the result of to_numpy never changes the data.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	data = ArrayData(values)
	numpy_copy = data.to_numpy()

	numpy_copy[FIRST_POSITION] = CHANGED_VALUE

	stored_rows = values.tolist()
	assert stored_rows == GRID


def test_array_data_reads_the_values_of_another_array_as_operand() -> None:
	"""
	Check that an Array operand gives its numpy values.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	other_values = numpy.array(DECIMALS)
	data = ExposedArrayData(values)
	other = ArrayData(other_values)

	operand = data.read_operand(other)

	assert operand is other_values


def test_array_data_rejects_a_list_as_operand() -> None:
	"""
	Check that a list operand raises UnsupportedOperandError.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	data = ExposedArrayData(values)

	with pytest.raises(UnsupportedOperandError):
		data.read_operand(REJECTED_OPERAND)


def test_array_data_combines_with_itself_on_the_left(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that a combination puts the Array values on the left and wraps the result.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the combination with a fake recording its operands.
	"""
	recorder = OperandRecorder()
	monkeypatch.setattr(array_data, COMBINE_VALUES_NAME, recorder.combine)
	values = numpy.array(GRID)
	data = ExposedArrayData(values)

	combined = data.combine(SINGLE_VALUE)

	combined_values = combined.to_numpy()
	combined_list = combined_values.tolist()
	assert recorder.operands == [values, SINGLE_VALUE]
	assert combined_list == EXPECTED_FAKE_RESULT


def test_array_data_combines_with_itself_on_the_right(monkeypatch: pytest.MonkeyPatch) -> None:
	"""
	Check that a reflected combination puts the single value on the left.

	.. versionadded:: 0.1.0

	Parameters
	----------
	monkeypatch
		Replaces the combination with a fake recording its operands.
	"""
	recorder = OperandRecorder()
	monkeypatch.setattr(array_data, COMBINE_VALUES_NAME, recorder.combine)
	values = numpy.array(GRID)
	data = ExposedArrayData(values)

	data.combine_reflected(SINGLE_VALUE)

	assert recorder.operands == [SINGLE_VALUE, values]

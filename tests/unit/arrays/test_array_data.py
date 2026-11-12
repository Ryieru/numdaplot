"""
Unit tests of ArrayData.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from datetime import time
from typing import Any, Self

import numpy
import pytest
from numpy.typing import NDArray

import numdaplot as ndp
from numdaplot.arrays import array_data
from numdaplot.arrays.array_data import ArrayData, read_stored_values
from numdaplot.arrays.operations.operand import Operand
from numdaplot.data_types.type import Type
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.shapes.shape import Shape

GRID = [[1, 2, 3], [4, 5, 6]]
GRID_SHAPE = Shape([2, 3])
DECIMALS = [1.5]
SINGLE_VALUE = 10
REJECTED_OPERAND = [1, 2]
SUBTRACTION_SYMBOL = "-"
COMBINE_VALUES_NAME = "combine_values"
FAKE_RESULT = numpy.array([7, 7])
EXPECTED_FAKE_RESULT = [7, 7]
TIME_ARRAY = ndp.Array.from_list([time(0, 1), None])
STORED_TIME_DTYPE_NAME = "timedelta64[us]"


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


def test_array_data_refuses_its_constructor() -> None:
	"""
	Check that creating ArrayData by its constructor raises RefusedOperationError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError):
		ArrayData()


def test_array_data_create_stores_the_values_without_copy() -> None:
	"""
	Check that _create keeps the given numpy values themselves.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)

	data = ArrayData._create(values)

	assert data._values is values


def test_array_data_reads_its_shape() -> None:
	"""
	Check that the shape is a Shape of the stored values.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	data = ArrayData._create(values)

	assert data.shape == GRID_SHAPE


def test_array_data_reads_its_type() -> None:
	"""
	Check that the type is the numdaplot type of the stored values.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(DECIMALS)
	data = ArrayData._create(values)

	assert data.dtype == Type.FLOAT64


def test_array_data_makes_its_values_read_only() -> None:
	"""
	Check that the stored values cannot be written.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)

	ArrayData._create(values)

	assert not values.flags.writeable


def test_array_data_reads_the_values_of_another_array_as_operand() -> None:
	"""
	Check that an Array operand gives its numpy values.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array(GRID)
	other_values = numpy.array(DECIMALS)
	data = ExposedArrayData._create(values)
	other = ArrayData._create(other_values)

	operand = data.read_operand(other)

	assert operand is other_values


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
	data = ExposedArrayData._create(values)

	combined = data.combine(SINGLE_VALUE)

	combined_values = read_stored_values(combined)
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
	data = ExposedArrayData._create(values)

	data.combine_reflected(SINGLE_VALUE)

	assert recorder.operands == [SINGLE_VALUE, values]


def test_read_stored_values_keeps_the_storage_of_times() -> None:
	"""
	Check that the stored values stay in microseconds.

	.. versionadded:: 0.1.0
	"""
	stored_values = read_stored_values(TIME_ARRAY)

	assert stored_values.dtype.name == STORED_TIME_DTYPE_NAME

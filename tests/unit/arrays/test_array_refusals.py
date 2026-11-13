"""
Unit tests of ArrayRefusals.

.. versionadded:: 0.1.0
"""

# The tests create the objects from their stored values, with the creation reserved to numdaplot.
# pyright: reportPrivateUsage=false

from collections.abc import Callable

import numpy
import pytest

from numdaplot.arrays.array_refusals import ArrayRefusals, refuse_comparison
from numdaplot.errors.settings.refused_operation_error import RefusedOperationError

VALUES = [1, 2]
OTHER = 1
LESS_SYMBOL = "<"
ALTERNATIVE = "select"
EXPECTED_COMPARISON_MESSAGE = "Comparing an Array with < is not available, use select instead."
type RefusedOperation = Callable[[ArrayRefusals], object]
REFUSED_OPERATIONS = list[RefusedOperation](
	[
		lambda array: array == OTHER,
		lambda array: array != OTHER,
		lambda array: array < OTHER,
		lambda array: array <= OTHER,
		lambda array: array > OTHER,
		lambda array: array >= OTHER,
		lambda array: array[0],
		lambda array: array.__setitem__(0, OTHER),
		lambda array: list(array),
		lambda array: OTHER in array,
		lambda array: len(array),
		lambda array: bool(array),
		lambda array: array @ array,
		lambda array: array.__rmatmul__(OTHER),
	]
)


@pytest.mark.parametrize("refused_operation", REFUSED_OPERATIONS)
def test_array_refusals_refuse_each_python_operation(refused_operation: RefusedOperation) -> None:
	"""
	Check that each refused Python operation raises RefusedOperationError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	refused_operation
		A function applying one refused operation to an Array.
	"""
	values = numpy.array(VALUES)
	array = ArrayRefusals._create(values)

	with pytest.raises(RefusedOperationError):
		refused_operation(array)


def test_refuse_comparison_names_the_operator_and_the_alternative() -> None:
	"""
	Check the message of a refused comparison.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(RefusedOperationError) as error_information:
		refuse_comparison(LESS_SYMBOL, ALTERNATIVE)

	error_text = str(error_information.value)
	assert error_text == EXPECTED_COMPARISON_MESSAGE


def test_array_refusals_are_not_hashable() -> None:
	"""
	Check that an Array cannot be a dictionary key, since == is refused.

	.. versionadded:: 0.1.0
	"""
	assert ArrayRefusals.__hash__ is None

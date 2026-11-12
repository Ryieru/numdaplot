"""
Unit tests of Array.

.. versionadded:: 0.1.0
"""

import numpy
import pytest

from numdaplot.arrays.array import Array, create_array
from numdaplot.arrays.array_arithmetic import ArrayArithmetic
from numdaplot.arrays.array_calculation import ArrayCalculation
from numdaplot.arrays.array_creation import ArrayCreation
from numdaplot.arrays.array_exchange import ArrayExchange
from numdaplot.arrays.array_layout import ArrayLayout
from numdaplot.arrays.array_logic import ArrayLogic
from numdaplot.arrays.array_reflected_arithmetic import ArrayReflectedArithmetic
from numdaplot.arrays.array_refusals import ArrayRefusals
from numdaplot.arrays.array_selection import ArraySelection
from numdaplot.data_types.type import Type

METHOD_GROUPS = [
	ArrayCreation,
	ArrayExchange,
	ArraySelection,
	ArrayCalculation,
	ArrayLayout,
	ArrayArithmetic,
	ArrayReflectedArithmetic,
	ArrayLogic,
	ArrayRefusals,
]
VALUES = [1, 2]
FACTOR = 2
STORED_TIMES = numpy.array([60000000], dtype="timedelta64[us]")


@pytest.mark.parametrize("method_group", METHOD_GROUPS)
def test_array_offers_every_group_of_methods(method_group: type) -> None:
	"""
	Check that Array inherits each group of methods.

	.. versionadded:: 0.1.0

	Parameters
	----------
	method_group
		A group of Array methods.
	"""
	assert issubclass(Array, method_group)


def test_array_operations_return_arrays() -> None:
	"""
	Check that an operation inherited from a group returns an Array, not the group class.

	.. versionadded:: 0.1.0
	"""
	array = Array.from_list(VALUES)

	doubled_array = array * FACTOR

	assert type(doubled_array) is Array


def test_create_array_keeps_times_of_day() -> None:
	"""
	Check that stored microseconds stay times of day, unlike from_numpy.

	.. versionadded:: 0.1.0
	"""
	time_array = create_array(STORED_TIMES)

	assert time_array.dtype == Type.TIME

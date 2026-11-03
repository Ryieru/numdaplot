"""
Unit tests of Array.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.arrays.array import Array
from numdaplot.arrays.array_arithmetic import ArrayArithmetic
from numdaplot.arrays.array_calculation import ArrayCalculation
from numdaplot.arrays.array_conversion import ArrayConversion
from numdaplot.arrays.array_creation import ArrayCreation
from numdaplot.arrays.array_layout import ArrayLayout
from numdaplot.arrays.array_logic import ArrayLogic
from numdaplot.arrays.array_reflected_arithmetic import ArrayReflectedArithmetic
from numdaplot.arrays.array_refusals import ArrayRefusals
from numdaplot.arrays.array_selection import ArraySelection

METHOD_GROUPS = [
	ArrayCreation,
	ArrayConversion,
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

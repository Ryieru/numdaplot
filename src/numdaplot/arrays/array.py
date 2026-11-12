"""
The ``ndp.Array`` class: values of one type in one or several dimensions.

.. versionadded:: 0.1.0
"""

from typing import Any

from numpy.typing import NDArray

from numdaplot.arrays.array_arithmetic import ArrayArithmetic
from numdaplot.arrays.array_calculation import ArrayCalculation
from numdaplot.arrays.array_creation import ArrayCreation
from numdaplot.arrays.array_display import ArrayDisplay
from numdaplot.arrays.array_exchange import ArrayExchange
from numdaplot.arrays.array_layout import ArrayLayout
from numdaplot.arrays.array_logic import ArrayLogic
from numdaplot.arrays.array_reflected_arithmetic import ArrayReflectedArithmetic
from numdaplot.arrays.array_refusals import ArrayRefusals
from numdaplot.arrays.array_selection import ArraySelection
from numdaplot.arrays.array_type_change import ArrayTypeChange


class Array(
	ArrayCreation,
	ArrayExchange,
	ArrayTypeChange,
	ArraySelection,
	ArrayCalculation,
	ArrayLayout,
	ArrayArithmetic,
	ArrayReflectedArithmetic,
	ArrayLogic,
	ArrayDisplay,
	ArrayRefusals,
):
	"""
	Values of one type in one or several dimensions, wrapping a numpy array.

	An Array never changes: every operation returns a new Array.

	- Create it with ``from_list``, ``from_numpy``, ``filled``, ``from_range``, ``from_spacing``, ``from_date_parts``
	  or ``random``.
	- Combine it with ``+``, ``-``, ``*``, ``/``, ``//``, ``%``, ``**``, and booleans with ``&``, ``|``, ``~``.
	- Select values with ``select``, ``check``, ``take`` and ``replace``.
	- Compute with ``compute`` and ``apply``.
	- Rearrange it with ``reshape``, ``transpose``, ``flatten``, ``sort`` and ``unique``.
	- Read it with ``shape``, ``dtype``, ``to_list``, ``to_value``, ``to_numpy`` and ``is_equal``.
	- Change the type of its values with ``convert``.

	Calling ``ndp.Array(...)``, comparisons, brackets, ``for``, ``in``, ``len``, ``bool`` and ``@`` are refused
	with ``RefusedOperationError``, which names the method to use instead.

	.. versionadded:: 0.1.0

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.5, 8.0, 30.0])
	>>> prices
	Array([12.5,  8. , 30. ], dtype=FLOAT64)
	>>> prices.shape
	Shape(dimensions=[3])
	>>> prices.dtype
	<Type.FLOAT64: 10>
	"""


def create_array(values: NDArray[Any]) -> Array:
	"""
	Return an Array holding values already stored as numdaplot stores them, for the code of numdaplot.

	Unlike ``Array.from_numpy``, durations in microseconds stay times of day.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Values in the numpy dtype of a numdaplot type, kept without copy.

	Returns
	-------
	Array
		The new Array.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.array import create_array
	>>> create_array(numpy.array([60000000], dtype="timedelta64[us]"))
	Array(['00:01:00'], dtype=TIME)
	"""
	# The function lives next to the class to create Arrays on behalf of the rest of numdaplot.
	created_array = Array._create(values)  # pyright: ignore[reportPrivateUsage]

	return created_array

"""
The ``ndp.Array`` class: values of one type in one or several dimensions.

.. versionadded:: 0.1.0
"""

from numdaplot.arrays.array_arithmetic import ArrayArithmetic
from numdaplot.arrays.array_calculation import ArrayCalculation
from numdaplot.arrays.array_conversion import ArrayConversion
from numdaplot.arrays.array_creation import ArrayCreation
from numdaplot.arrays.array_layout import ArrayLayout
from numdaplot.arrays.array_logic import ArrayLogic
from numdaplot.arrays.array_reflected_arithmetic import ArrayReflectedArithmetic
from numdaplot.arrays.array_refusals import ArrayRefusals
from numdaplot.arrays.array_selection import ArraySelection


class Array(
	ArrayCreation,
	ArrayConversion,
	ArraySelection,
	ArrayCalculation,
	ArrayLayout,
	ArrayArithmetic,
	ArrayReflectedArithmetic,
	ArrayLogic,
	ArrayRefusals,
):
	"""
	Values of one type in one or several dimensions, wrapping a numpy array.

	An Array never changes: every operation returns a new Array.

	- Create it with ``from_list``, ``from_numpy``, ``filled``, ``from_range``, ``from_spacing`` or ``random``.
	- Combine it with ``+``, ``-``, ``*``, ``/``, ``//``, ``%``, ``**``, and booleans with ``&``, ``|``, ``~``.
	- Select values with ``select``, ``check``, ``take`` and ``replace``.
	- Compute with ``compute`` and ``apply``.
	- Rearrange it with ``reshape``, ``transpose``, ``flatten``, ``sort`` and ``unique``.
	- Read it with ``shape``, ``dtype``, ``to_list``, ``to_value``, ``to_numpy`` and ``is_equal``.

	Comparisons, brackets, ``for``, ``in``, ``len``, ``bool`` and ``@`` are refused with ``RefusedOperationError``,
	which names the method to use instead.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The numpy values, stored without copy. Reserved to numdaplot: create an Array with
		``from_list``, ``from_numpy``, ``filled``, ``from_range``, ``from_spacing`` or ``random``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> prices = ndp.Array.from_list([12.5, 8.0, 30.0])
	>>> prices
	Array([12.5,  8. , 30. ], dtype=FLOAT64)
	>>> prices.shape
	Shape(dimensions=(3,))
	>>> prices.dtype
	<Type.FLOAT64: 10>
	"""

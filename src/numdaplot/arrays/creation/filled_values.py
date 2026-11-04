"""
Values made of a single repeated value.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.creation.list_conversion import convert_list
from numdaplot.arrays.shape import Shape
from numdaplot.data_types.type import Type
from numdaplot.rules.rule_values import ScalarValue


def build_filled_values(shape: Shape, value: ScalarValue, dtype: Type | None) -> NDArray[Any]:
	"""
	Return numpy values of a shape, all equal to one value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	shape
		The shape of the result.
	value
		The repeated value.
	dtype
		The type to store the value as, guessed from the value when ``None``.

	Returns
	-------
	NDArray
		The filled values.

	Raises
	------
	ValueConversionError
		When the value cannot be stored as ``dtype`` without losing information.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.creation.filled_values import build_filled_values
	>>> build_filled_values(ndp.Shape((2, 3)), 0, None)
	array([[0, 0, 0],
	       [0, 0, 0]])
	"""
	single_value_list = list[object]([value])
	stored_value = convert_list(single_value_list, dtype)
	single_stored_value = stored_value[0]
	filled_values = numpy.full(shape.dimensions, single_stored_value, dtype=stored_value.dtype)

	return filled_values

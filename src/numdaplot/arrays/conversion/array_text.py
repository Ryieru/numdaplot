"""
Text shown for an Array.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.data_types.numpy_mapping import from_numpy_dtype

ARRAY_PREFIX = "Array("
ARRAY_TEXT = ARRAY_PREFIX + "{values}, dtype={type_name})"
VALUE_SEPARATOR = ", "


def format_array(values: NDArray[Any]) -> str:
	"""
	Return the text of an Array: its values as nested lists, then its type.

	Rows of a two-dimensional Array are aligned on separate lines, and long Arrays are shortened with ``...``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.

	Returns
	-------
	str
		The text, such as ``Array([1, 2, 3], dtype=INT64)``.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.conversion.array_text import format_array
	>>> format_array(numpy.array([1, 2, 3]))
	'Array([1, 2, 3], dtype=INT64)'
	"""
	array_type = from_numpy_dtype(values.dtype)
	values_text = numpy.array2string(values, separator=VALUE_SEPARATOR, prefix=ARRAY_PREFIX)
	array_text = ARRAY_TEXT.format(values=values_text, type_name=array_type.name)

	return array_text

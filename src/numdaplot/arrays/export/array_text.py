"""
Text shown for an Array.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.column_storage.time_text import format_datetimes, format_durations, format_times
from numdaplot.types.numpy_mapping import from_numpy_dtype
from numdaplot.types.type import Type

ARRAY_PREFIX = "Array("
ARRAY_TEXT = ARRAY_PREFIX + "{values}, dtype={type_name})"
VALUE_SEPARATOR = ", "


def format_array(values: NDArray[Any]) -> str:
	"""
	Return the text of an Array: its values as nested lists, then its type.

	Rows of a two-dimensional Array are aligned on separate lines, and long Arrays are shortened with ``...``.
	Datetimes are written as ``"2026-01-02 10:30:00"``, durations as pandas writes them, ``"1 days 12:00:00"``, and
	times of day as ``"15:35:00"``.

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
	>>> from numdaplot.arrays.export.array_text import format_array
	>>> format_array(numpy.array([1, 2, 3]))
	'Array([1, 2, 3], dtype=INT64)'
	"""
	array_type = from_numpy_dtype(values.dtype)
	shown_values = values
	if array_type == Type.DATETIME:
		shown_values = format_datetimes(values)

	if array_type == Type.DURATION:
		shown_values = format_durations(values)

	if array_type == Type.TIME:
		shown_values = format_times(values)

	values_text = numpy.array2string(shown_values, separator=VALUE_SEPARATOR, prefix=ARRAY_PREFIX)
	array_text = ARRAY_TEXT.format(values=values_text, type_name=array_type.name)

	return array_text

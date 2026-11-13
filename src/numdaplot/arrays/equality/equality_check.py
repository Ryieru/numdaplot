"""
Comparison of the values of two Arrays.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.equality.type_match import TypeMatch
from numdaplot.arrays.selection.missing_mask import find_missing
from numdaplot.types.numpy_mapping import from_numpy_dtype
from numdaplot.types.type import Type
from numdaplot.types.value_family import find_family


def match_types(left_type: Type, right_type: Type, types: TypeMatch) -> bool:
	"""
	Return whether values of two types may be equal: of the same family, and of the same type with ``TypeMatch.STRICT``.

	.. versionadded:: 0.2.0

	Parameters
	----------
	left_type
		The type of the first values.
	right_type
		The type of the second values.
	types
		Whether the types must also be the same.

	Returns
	-------
	bool
		False for types of different families, such as numbers and texts, or for different types when they must match.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.equality.equality_check import match_types
	>>> match_types(ndp.Type.INT64, ndp.Type.FLOAT64, ndp.TypeMatch.IGNORED)
	True
	>>> match_types(ndp.Type.INT64, ndp.Type.FLOAT64, ndp.TypeMatch.STRICT)
	False
	"""
	different_types = left_type != right_type
	rejects_different_types = types == TypeMatch.STRICT and different_types
	if rejects_different_types:
		return False

	left_family = find_family(left_type)
	right_family = find_family(right_type)
	same_family = left_family == right_family

	return same_family


def are_equal(left: NDArray[Any], right: NDArray[Any], types: TypeMatch) -> bool:
	"""
	Return whether two Arrays hold the same values at the same positions.

	Two missing values at the same position are equal. Values of types that cannot be compared,
	such as numbers and texts, are never equal.

	.. versionadded:: 0.1.0

	Parameters
	----------
	left
		The values of the first Array.
	right
		The values of the second Array.
	types
		Whether the types must also be the same.

	Returns
	-------
	bool
		True when the shapes and the values are the same, and the types too with ``TypeMatch.STRICT``.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.equality.equality_check import are_equal
	>>> are_equal(numpy.array([1, 2]), numpy.array([1.0, 2.0]), ndp.TypeMatch.IGNORED)
	True
	"""
	if left.shape != right.shape:
		return False

	left_type = from_numpy_dtype(left.dtype)
	right_type = from_numpy_dtype(right.dtype)
	types_match = match_types(left_type, right_type, types)
	if not types_match:
		return False

	same_values = left == right
	left_missing = find_missing(left)
	right_missing = find_missing(right)
	both_missing = left_missing & right_missing
	equal_positions = same_values | both_missing
	all_equal = numpy.all(equal_positions)
	is_equal = bool(all_equal)

	return is_equal

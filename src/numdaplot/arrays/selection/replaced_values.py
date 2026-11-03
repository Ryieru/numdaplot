"""
Replacement of the values of a region of an Array.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.operations.operand import Operand, find_operand_type
from numdaplot.arrays.selection.region_index import build_region_index
from numdaplot.data_types.numpy_mapping import from_numpy_dtype, to_numpy_dtype
from numdaplot.errors.shape_mismatch_error import ShapeMismatchError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.positions.region import Region

SAFE_CASTING = "same_kind"


def replace_region(values: NDArray[Any], region: Region, new_values: Operand) -> NDArray[Any]:
	"""
	Return a copy of the values whose region is replaced.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	region
		The positions to replace.
	new_values
		A single value written at every position, or Array values of exactly the shape of the region.

	Returns
	-------
	NDArray
		The new values, of the same shape and type.

	Raises
	------
	ShapeMismatchError
		When Array values do not have the shape of the region.
	ValueConversionError
		When the new values cannot be stored in the type of the values without losing information.
	DimensionError, RefusedOperationError, InvalidPositionError
		When the region does not fit the values, as in ``build_region_index``.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.selection.replaced_values import replace_region
	>>> replace_region(numpy.array([1, 2, 3]), ndp.Region(rows=ndp.Index(0)), 9)
	array([9, 2, 3])
	"""
	region_index = build_region_index(region, values.shape)
	region_values = values[region_index]
	if isinstance(new_values, numpy.ndarray):
		if new_values.shape != region_values.shape:
			raise ShapeMismatchError(new_values.shape, region_values.shape)

	require_storable(new_values, values)
	replaced_values = values.copy()
	# numpy reads dates and durations from Python objects, which its type hints do not list.
	storable_values = cast(Any, new_values)
	try:
		replaced_values[region_index] = storable_values
	except OverflowError as error:
		new_type = find_operand_type(new_values)
		values_type = from_numpy_dtype(values.dtype)
		raise ValueConversionError(new_type.name, values_type.name) from error

	return replaced_values


def require_storable(new_values: Operand, values: NDArray[Any]) -> None:
	"""
	Check that new values can be stored in the type of existing values without losing information.

	.. versionadded:: 0.1.0

	Parameters
	----------
	new_values
		A single value, or Array values.
	values
		The values receiving them.

	Raises
	------
	ValueConversionError
		When a decimal would become an integer, or a text a number, for example.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.selection.replaced_values import require_storable
	>>> require_storable(2, numpy.array([1.5]))
	"""
	new_type = find_operand_type(new_values)
	values_type = from_numpy_dtype(values.dtype)
	new_dtype = to_numpy_dtype(new_type)
	is_safe = numpy.can_cast(new_dtype, values.dtype, casting=SAFE_CASTING)
	if not is_safe:
		raise ValueConversionError(new_type.name, values_type.name)

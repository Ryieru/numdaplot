"""
Comparison of the values of an Array with the values at the same positions of another Array.

.. versionadded:: 0.2.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.array_data import ArrayData, read_stored_values
from numdaplot.arrays.selection.missing_mask import find_missing
from numdaplot.errors.positions.shape_mismatch_error import ShapeMismatchError
from numdaplot.errors.types.incompatible_types_error import IncompatibleTypesError
from numdaplot.types.numpy_mapping import from_numpy_dtype
from numdaplot.types.value_family import find_family


def compare_with_array(
	values: NDArray[Any], reference: ArrayData, compare: numpy.ufunc, operation: str
) -> NDArray[numpy.bool_]:
	"""
	Return the comparison of each value with the value at the same position of a reference Array.

	A missing reference value matches nothing. A missing tested value is not set apart.

	.. versionadded:: 0.2.0

	Parameters
	----------
	values
		The tested values.
	reference
		The Array of reference values, of the same shape.
	compare
		The numpy comparison, such as ``numpy.equal``, with the tested values on its left.
	operation
		The name of the rule, shown in the errors.

	Returns
	-------
	NDArray[numpy.bool_]
		The result at each position, False where the reference value is missing.

	Raises
	------
	ShapeMismatchError
		When the reference Array does not have the shape of the values.
	IncompatibleTypesError
		When the reference values belong to another family than the values, such as texts and numbers.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.rules.array_reference import compare_with_array
	>>> from numdaplot.arrays.array_data import read_stored_values
	>>> departures = read_stored_values(ndp.Array.from_list(["Pau", "Lyon", "Dax"]))
	>>> arrivals = ndp.Array.from_list(["Pau", None, "Nice"])
	>>> compare_with_array(departures, arrivals, numpy.equal, "Equal")
	array([ True, False, False])
	"""
	reference_values = read_stored_values(reference)
	if reference_values.shape != values.shape:
		raise ShapeMismatchError(values.shape, reference_values.shape)

	require_comparable_values(values, reference_values, operation)
	matches = compare(values, reference_values)
	reference_missing = find_missing(reference_values)
	present_matches = matches & ~reference_missing

	return present_matches


def require_comparable_values(values: NDArray[Any], reference_values: NDArray[Any], operation: str) -> None:
	"""
	Check that two sets of values belong to the same family of types, so that they can be compared.

	.. versionadded:: 0.2.0

	Parameters
	----------
	values
		The tested values.
	reference_values
		The reference values.
	operation
		The name of the rule, shown in the error.

	Raises
	------
	IncompatibleTypesError
		When the two sets of values belong to different families, such as texts and numbers.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.rules.array_reference import require_comparable_values
	>>> from numdaplot.arrays.array_data import read_stored_values
	>>> texts = read_stored_values(ndp.Array.from_list(["a", "b"]))
	>>> try:
	... 	require_comparable_values(numpy.array([1, 2]), texts, "Greater")
	... except ndp.IncompatibleTypesError as error:
	... 	print(error)
	Cannot apply Greater to INT64 and TEXT.
	"""
	value_type = from_numpy_dtype(values.dtype)
	reference_type = from_numpy_dtype(reference_values.dtype)
	value_family = find_family(value_type)
	reference_family = find_family(reference_type)
	if value_family != reference_family:
		raise IncompatibleTypesError(operation, [value_type.name, reference_type.name])

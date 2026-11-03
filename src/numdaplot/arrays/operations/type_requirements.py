"""
Checks that the values of an Array have a type an operation applies to.

.. versionadded:: 0.1.0
"""

from typing import Any

from numpy.typing import NDArray

from numdaplot.data_types.numpy_mapping import from_numpy_dtype
from numdaplot.data_types.value_family import ValueFamily, find_family
from numdaplot.data_types.value_type import find_value_type
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.rules.rule_values import ScalarValue


def require_family(values: NDArray[Any], accepted_families: frozenset[ValueFamily], operation: str) -> None:
	"""
	Check that the values of an Array belong to one of the families an operation applies to.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	accepted_families
		The families the operation applies to.
	operation
		Name of the operation, shown in the error message.

	Raises
	------
	IncompatibleTypesError
		When the type of the values belongs to another family.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.type_requirements import require_family
	>>> from numdaplot.data_types.value_family import ValueFamily
	>>> require_family(numpy.array([1.5]), frozenset({ValueFamily.NUMBER}), "Mean")
	"""
	array_type = from_numpy_dtype(values.dtype)
	array_family = find_family(array_type)
	if array_family not in accepted_families:
		raise IncompatibleTypesError(operation, [array_type.name])


def require_comparable(values: NDArray[Any], reference: ScalarValue, operation: str) -> None:
	"""
	Check that the values of an Array can be compared with a reference value.

	Numbers compare with numbers, texts with texts, dates and datetimes with each other.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	reference
		The value they are compared with.
	operation
		Name of the operation, shown in the error message.

	Raises
	------
	IncompatibleTypesError
		When the reference value belongs to another family than the values.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.operations.type_requirements import require_comparable
	>>> require_comparable(numpy.array([1, 2]), 1.5, "Greater")
	"""
	array_type = from_numpy_dtype(values.dtype)
	reference_type = find_value_type(reference)
	array_family = find_family(array_type)
	reference_family = find_family(reference_type)
	if array_family != reference_family:
		raise IncompatibleTypesError(operation, [array_type.name, reference_type.name])

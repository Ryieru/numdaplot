"""
Conversion of Python values to numpy values of a numdaplot type.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.arrays.creation.list_shape import find_list_shape, flatten_list
from numdaplot.data_types.numpy_mapping import to_numpy_dtype
from numdaplot.data_types.type import Type
from numdaplot.data_types.value_type import find_common_type, find_value_type
from numdaplot.errors.missing_type_error import MissingTypeError
from numdaplot.errors.unsupported_missing_error import UnsupportedMissingError
from numdaplot.errors.value_conversion_error import ValueConversionError

FROM_LIST_OPERATION = "from_list"
SAFE_CASTING = "same_kind"
WHOLE_NUMBER_KINDS = frozenset({"i", "u"})
NOT_A_TIME = "NaT"
NANOSECOND_UNIT = "ns"
MISSING_MARKERS = {
	Type.FLOAT32: numpy.nan,
	Type.FLOAT64: numpy.nan,
	Type.TEXT: numpy.nan,
	Type.DATE: numpy.datetime64(NOT_A_TIME, NANOSECOND_UNIT),
	Type.DATETIME: numpy.datetime64(NOT_A_TIME, NANOSECOND_UNIT),
	Type.DURATION: numpy.timedelta64(NOT_A_TIME, NANOSECOND_UNIT),
}


def convert_list(values: list[object], dtype: Type | None) -> NDArray[Any]:
	"""
	Return the numpy values of nested Python lists, stored as a numdaplot type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		A list of single values or of nested lists. ``None`` is a missing value.
	dtype
		The type to store the values as, guessed from the values when ``None``.

	Returns
	-------
	NDArray
		The values, with one dimension per nesting level.

	Raises
	------
	IrregularListError
		When nested lists do not form a regular block.
	IncompatibleTypesError
		When the values mix several families of types, such as numbers and texts.
	MissingTypeError
		When ``dtype`` is ``None`` and there is no present value to guess the type from.
	UnsupportedMissingError
		When a value is missing and the type cannot hold missing values.
	ValueConversionError
		When the values cannot be stored as ``dtype`` without losing information.

	Examples
	--------
	>>> from numdaplot.arrays.creation.list_conversion import convert_list
	>>> convert_list([[1, 2], [3, 4.5]], None)
	array([[1. , 2. ],
	       [3. , 4.5]])
	"""
	dimensions = find_list_shape(values)
	single_values = flatten_list(values)
	guessed_type = guess_list_type(single_values)
	stored_type = choose_stored_type(guessed_type, dtype)
	marked_values = mark_missing_values(single_values, stored_type)
	stored_values = store_values(marked_values, guessed_type, stored_type)
	shaped_values = stored_values.reshape(dimensions)

	return shaped_values


def guess_list_type(single_values: list[object]) -> Type | None:
	"""
	Return the type holding every present value of a flat list.

	.. versionadded:: 0.1.0

	Parameters
	----------
	single_values
		Single values, ``None`` being a missing value.

	Returns
	-------
	Type or None
		The common type of the present values, or ``None`` when no value is present.

	Raises
	------
	IncompatibleTypesError
		When the values mix several families of types.

	Examples
	--------
	>>> from numdaplot.arrays.creation.list_conversion import guess_list_type
	>>> guess_list_type([1, None, 2.5])
	<Type.FLOAT64: 10>
	"""
	value_types = [find_value_type(value) for value in single_values if value is not None]
	type_count = len(value_types)
	if type_count == 0:
		return None

	common_type = find_common_type(value_types, FROM_LIST_OPERATION)

	return common_type


def choose_stored_type(guessed_type: Type | None, dtype: Type | None) -> Type:
	"""
	Return the type the values are stored as: the given one, or else the guessed one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	guessed_type
		The type guessed from the present values, ``None`` when no value is present.
	dtype
		The type given by the user, ``None`` when omitted.

	Returns
	-------
	Type
		``dtype`` when given, otherwise ``guessed_type``.

	Raises
	------
	MissingTypeError
		When both types are ``None``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.creation.list_conversion import choose_stored_type
	>>> choose_stored_type(ndp.Type.INT64, ndp.Type.FLOAT32)
	<Type.FLOAT32: 9>
	"""
	if dtype is not None:
		return dtype

	if guessed_type is None:
		raise MissingTypeError()

	return guessed_type


def mark_missing_values(single_values: list[object], stored_type: Type) -> list[object]:
	"""
	Replace each ``None`` with the missing value marker of a type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	single_values
		Single values, ``None`` being a missing value.
	stored_type
		The type the values are stored as.

	Returns
	-------
	list[object]
		The values, with NaN for decimals and NaT for dates and durations instead of ``None``.

	Raises
	------
	UnsupportedMissingError
		When a value is missing and the type has no missing value marker.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.creation.list_conversion import mark_missing_values
	>>> mark_missing_values([1.5, None], ndp.Type.FLOAT64)
	[1.5, nan]
	"""
	has_missing_value = None in single_values
	if not has_missing_value:
		return single_values

	if stored_type not in MISSING_MARKERS:
		raise UnsupportedMissingError(stored_type.name)

	missing_marker = MISSING_MARKERS[stored_type]
	marked_values = [missing_marker if value is None else value for value in single_values]

	return marked_values


def store_values(marked_values: list[object], guessed_type: Type | None, stored_type: Type) -> NDArray[Any]:
	"""
	Return the values as a flat numpy array of the stored type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	marked_values
		Single values whose missing values are already replaced with markers.
	guessed_type
		The type guessed from the present values, ``None`` when no value is present.
	stored_type
		The type the values are stored as.

	Returns
	-------
	NDArray
		A one-dimensional array of the stored type.

	Raises
	------
	UnsupportedTypeError
		When the stored type has no numpy equivalent, which is the case of ``CATEGORY``.
	ValueConversionError
		When the guessed type cannot be stored as the stored type without losing information,
		or when a value exceeds the range of the stored type, such as -1 stored as ``UINT8``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.creation.list_conversion import store_values
	>>> store_values([1, 2], ndp.Type.INT64, ndp.Type.FLOAT64)
	array([1., 2.])
	>>> store_values([1, 2], ndp.Type.INT64, ndp.Type.UINT8)
	array([1, 2], dtype=uint8)
	"""
	stored_dtype = to_numpy_dtype(stored_type)
	if guessed_type is None:
		values_without_present_value = numpy.array(marked_values, dtype=stored_dtype)
		return values_without_present_value

	guessed_dtype = to_numpy_dtype(guessed_type)
	is_safe = numpy.can_cast(guessed_dtype, stored_dtype, casting=SAFE_CASTING)
	# Integers may be stored as unsigned integers: numpy then rejects each value out of range.
	is_whole_number_storage = guessed_dtype.kind in WHOLE_NUMBER_KINDS and stored_dtype.kind in WHOLE_NUMBER_KINDS
	is_storable = is_safe or is_whole_number_storage
	if not is_storable:
		raise ValueConversionError(guessed_type.name, stored_type.name)

	try:
		stored_values = numpy.array(marked_values, dtype=stored_dtype)
	except OverflowError as error:
		raise ValueConversionError(guessed_type.name, stored_type.name) from error

	return stored_values

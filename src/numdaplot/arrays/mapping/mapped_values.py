"""
Application of a ValueMapping to the values of an Array.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence
from datetime import date, datetime, time
from typing import Any, cast

from numpy.typing import NDArray

from numdaplot.arrays.conversion.python_values import to_python_list
from numdaplot.arrays.creation.list_conversion import convert_list
from numdaplot.arrays.mapping.unmatched import Unmatched
from numdaplot.arrays.mapping.value_mapping import MAPPING_OPERATION, ValueMapping, find_new_type
from numdaplot.arrays.operations.type_requirements import require_comparable
from numdaplot.arrays.selection.missing_mask import find_missing
from numdaplot.data_types.numpy_mapping import from_numpy_dtype
from numdaplot.data_types.type import Type
from numdaplot.errors.unmatched_value_error import UnmatchedValueError
from numdaplot.errors.unsupported_missing_error import UnsupportedMissingError
from numdaplot.rules.rule_values import ScalarValue

DECIMAL_ADVICE = "Give decimal new values, such as 10.0, which can be missing."
BOOLEAN_ADVICE = "Give texts as new values, which can be missing."
MIDNIGHT = time()
INTEGER_TYPES = frozenset(
	{Type.INT8, Type.INT16, Type.INT32, Type.INT64, Type.UINT8, Type.UINT16, Type.UINT32, Type.UINT64}
)


def map_values(values: NDArray[Any], mapping: ValueMapping) -> NDArray[Any]:
	"""
	Return the values of an Array replaced by the new values of a mapping, in the same shape.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.
	mapping
		The new value of each listed value, and what happens to the others.

	Returns
	-------
	NDArray
		The new values, stored with the type the new values share. Missing values stay missing.

	Raises
	------
	IncompatibleTypesError
		When the old values are not of the type family of the Array.
	UnmatchedValueError
		When a value has no new value and ``others`` is ``Unmatched.ERROR``.
	UnsupportedMissingError
		When the result holds integers or booleans and a missing value.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.mapping.mapped_values import map_values
	>>> mapping = ndp.ValueMapping(changes=[ndp.ValueChange(1, "Homme"), ndp.ValueChange(2, "Femme")])
	>>> map_values(numpy.array([[1, 2], [2, 1]]), mapping).tolist()
	[['Homme', 'Femme'], ['Femme', 'Homme']]
	"""
	for change in mapping.changes:
		require_comparable(values, change.old_value, MAPPING_OPERATION)

	flat_values = values.ravel()
	new_values = find_flat_new_values(flat_values, mapping)
	new_type = find_new_type(mapping.changes)
	require_missing_supported(new_values, new_type)
	stored_values = convert_list(new_values, new_type)
	shaped_values = stored_values.reshape(values.shape)

	return shaped_values


def find_flat_new_values(flat_values: NDArray[Any], mapping: ValueMapping) -> list[object]:
	"""
	Return the new value of each value of a flat Array, None for a missing one.

	.. versionadded:: 0.1.0

	Parameters
	----------
	flat_values
		The values of an Array in one dimension.
	mapping
		The new value of each listed value, and what happens to the others.

	Returns
	-------
	list[object]
		The new Python values, in order.

	Raises
	------
	UnmatchedValueError
		At the first value without new value, when ``others`` is ``Unmatched.ERROR``.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.mapping.mapped_values import find_flat_new_values
	>>> mapping = ndp.ValueMapping(changes=[ndp.ValueChange(1.0, "one")], others=ndp.Unmatched.MISSING)
	>>> find_flat_new_values(numpy.array([1.0, numpy.nan, 2.0]), mapping)
	['one', None, None]
	"""
	array_type = from_numpy_dtype(flat_values.dtype)
	new_value_by_old = dict[ScalarValue, ScalarValue | None]()
	for change in mapping.changes:
		lookup_value = find_lookup_value(change.old_value, array_type)
		new_value_by_old[lookup_value] = change.new_value

	missing = find_missing(flat_values)
	raw_missing = missing.tolist()
	is_missing_list = cast(list[bool], raw_missing)
	python_values = to_python_list(flat_values)
	new_values = list[object]()
	for value, is_missing in zip(python_values, is_missing_list, strict=True):
		if is_missing:
			new_values.append(None)
			continue

		if value in new_value_by_old:
			new_value = new_value_by_old[value]
			new_values.append(new_value)
			continue

		if mapping.others == Unmatched.ERROR:
			raise UnmatchedValueError(value)

		new_values.append(None)

	return new_values


def require_missing_supported(new_values: Sequence[object], new_type: Type | None) -> None:
	"""
	Check that a result of integers or booleans holds no missing value, with advice fitting a mapping.

	.. versionadded:: 0.1.0

	Parameters
	----------
	new_values
		The new Python values, None for a missing one.
	new_type
		The type the new values share, or None.

	Raises
	------
	UnsupportedMissingError
		When the type is an integer or boolean type and a new value is None.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.mapping.mapped_values import require_missing_supported
	>>> try:
	... 	require_missing_supported([10, None], ndp.Type.INT64)
	... except ndp.UnsupportedMissingError as error:
	... 	print(error)
	INT64 values cannot be missing in an Array. Give decimal new values, such as 10.0, which can be missing.
	"""
	has_missing = None in new_values
	if not has_missing:
		return

	if new_type in INTEGER_TYPES:
		raise UnsupportedMissingError(new_type.name, advice=DECIMAL_ADVICE)

	if new_type == Type.BOOL:
		raise UnsupportedMissingError(new_type.name, advice=BOOLEAN_ADVICE)


def find_lookup_value(old_value: ScalarValue, array_type: Type) -> ScalarValue:
	"""
	Return an old value written as the values of the Array are, so that a date finds a datetime at midnight.

	.. versionadded:: 0.1.0

	Parameters
	----------
	old_value
		An old value of a ``ValueChange``.
	array_type
		The type of the values of the Array.

	Returns
	-------
	ScalarValue
		A date as a datetime at midnight for ``DATETIME`` values, a datetime at midnight as a date for ``DATE``
		values, any other value unchanged.

	Examples
	--------
	>>> from datetime import date
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.mapping.mapped_values import find_lookup_value
	>>> find_lookup_value(date(2026, 12, 25), ndp.Type.DATETIME)
	datetime.datetime(2026, 12, 25, 0, 0)
	"""
	if array_type == Type.DATETIME:
		datetime_value = write_date_as_datetime(old_value)
		return datetime_value

	if array_type == Type.DATE:
		date_value = write_midnight_as_date(old_value)
		return date_value

	return old_value


def write_date_as_datetime(old_value: ScalarValue) -> ScalarValue:
	"""
	Return a date as the datetime at midnight of that day, any other value unchanged.

	.. versionadded:: 0.1.0

	Parameters
	----------
	old_value
		An old value of a ``ValueChange``.

	Returns
	-------
	ScalarValue
		The datetime at midnight, or the value itself.

	Examples
	--------
	>>> from datetime import date
	>>> from numdaplot.arrays.mapping.mapped_values import write_date_as_datetime
	>>> write_date_as_datetime(date(2026, 12, 25)), write_date_as_datetime(3)
	(datetime.datetime(2026, 12, 25, 0, 0), 3)
	"""
	if isinstance(old_value, datetime):
		return old_value

	if not isinstance(old_value, date):
		return old_value

	midnight = datetime.combine(old_value, MIDNIGHT)

	return midnight


def write_midnight_as_date(old_value: ScalarValue) -> ScalarValue:
	"""
	Return a datetime at midnight as its date, any other value unchanged.

	.. versionadded:: 0.1.0

	Parameters
	----------
	old_value
		An old value of a ``ValueChange``.

	Returns
	-------
	ScalarValue
		The date of a datetime at midnight, or the value itself, so that a datetime with a time finds no date.

	Examples
	--------
	>>> from datetime import datetime
	>>> from numdaplot.arrays.mapping.mapped_values import write_midnight_as_date
	>>> write_midnight_as_date(datetime(2026, 12, 25)), write_midnight_as_date(datetime(2026, 12, 25, 10))
	(datetime.date(2026, 12, 25), datetime.datetime(2026, 12, 25, 10, 0))
	"""
	if not isinstance(old_value, datetime):
		return old_value

	old_time = old_value.time()
	if old_time != MIDNIGHT:
		return old_value

	old_date = old_value.date()

	return old_date

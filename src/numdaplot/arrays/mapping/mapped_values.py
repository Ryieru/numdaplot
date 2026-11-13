"""
Application of a ValueMapping to the values of an Array.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence
from datetime import date, datetime, time
from typing import Any, cast

from numpy.typing import NDArray

from numdaplot.arrays.creation.list_conversion import convert_list
from numdaplot.arrays.export.python_values import to_python_list
from numdaplot.arrays.mapping.mapping_result import MappingResult
from numdaplot.arrays.mapping.value_mapping import MAPPING_OPERATION, ValueMapping, find_new_type
from numdaplot.arrays.operations.type_requirements import require_comparable
from numdaplot.arrays.selection.missing_mask import find_missing
from numdaplot.brackets.unmatched import Unmatched
from numdaplot.errors.settings.unmatched_value_error import UnmatchedValueError
from numdaplot.errors.types.unsupported_missing_error import UnsupportedMissingError
from numdaplot.rules.rule_values import ScalarValue
from numdaplot.types.number_types import DECIMAL_TYPES, INTEGER_TYPES
from numdaplot.types.numpy_mapping import from_numpy_dtype
from numdaplot.types.type import Type
from numdaplot.types.value_family import ValueFamily, find_family
from numdaplot.types.value_type import find_common_type

DECIMAL_ADVICE = "Give decimal new values, such as 10.0, which can be missing."
BOOLEAN_ADVICE = "Give texts as new values, which can be missing."
KEPT_DECIMAL_ADVICE = "Give decimal new values, such as 10.0, or convert the Array to FLOAT64 first."
KEPT_BOOLEAN_ADVICE = "Convert the Array to TEXT first."
MIDNIGHT = time()


def map_values(values: NDArray[Any], mapping: ValueMapping) -> NDArray[Any]:
	"""
	Return the values of an Array replaced by the new values of a mapping, in the same shape.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Keeps the values without ``ValueChange`` when ``others`` is ``Unmatched.KEEP``. Numbers given to an Array of
		numbers take its type. Only missing new values keep the type of the Array.

	Parameters
	----------
	values
		The values of an Array.
	mapping
		The new value of each listed value, and what happens to the others.

	Returns
	-------
	NDArray
		The new values, stored with the type ``find_result_type`` gives. Missing values stay missing.

	Raises
	------
	IncompatibleTypesError
		When the old values are not of the type family of the Array, or the kept values and the new values are of
		several families.
	UnmatchedValueError
		When a value has no new value and ``others`` is ``Unmatched.ERROR``.
	UnsupportedMissingError
		When the result holds integers or booleans and a missing value.
	ValueConversionError
		When a new number does not fit the number type of the Array, such as 1000 given to ``INT8`` values.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.mapping.mapped_values import map_values
	>>> mapping = ndp.ValueMapping(changes=[ndp.ValueChange(1, "Homme"), ndp.ValueChange(2, "Femme")])
	>>> map_values(numpy.array([[1, 2], [2, 1]]), mapping).tolist()
	[['Homme', 'Femme'], ['Femme', 'Homme']]
	"""
	mapping_result = find_mapping_result(values, mapping)
	require_missing_supported(mapping_result.new_values, mapping_result.result_type, mapping.others)
	stored_values = convert_list(mapping_result.new_values, mapping_result.result_type)
	shaped_values = stored_values.reshape(values.shape)

	return shaped_values


def find_mapping_result(values: NDArray[Any], mapping: ValueMapping) -> MappingResult:
	"""
	Return the new values of a mapping in one dimension, with the type of the result.

	.. versionadded:: 0.2.0

	Parameters
	----------
	values
		The values the mapping applies to, in any shape.
	mapping
		The new value of each listed value, and what happens to the others.

	Returns
	-------
	MappingResult
		The new Python values, None for a missing one, and the type ``find_result_type`` gives.

	Raises
	------
	IncompatibleTypesError
		When the old values are not of the type family of the values, or the kept values and the new values are of
		several families.
	UnmatchedValueError
		When a value has no new value and ``others`` is ``Unmatched.ERROR``.

	Examples
	--------
	>>> import numpy
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.mapping.mapped_values import find_mapping_result
	>>> mapping = ndp.ValueMapping(changes=[ndp.ValueChange(1, "Homme")], others=ndp.Unmatched.MISSING)
	>>> mapping_result = find_mapping_result(numpy.array([1, 2]), mapping)
	>>> mapping_result.new_values, mapping_result.result_type
	(['Homme', None], <Type.TEXT: 12>)
	"""
	for change in mapping.changes:
		require_comparable(values, change.old_value, MAPPING_OPERATION)

	flat_values = values.ravel()
	new_values = find_flat_new_values(flat_values, mapping)
	value_type = from_numpy_dtype(values.dtype)
	result_type = find_result_type(value_type, mapping)
	mapping_result = MappingResult(new_values=new_values, result_type=result_type)

	return mapping_result


def find_flat_new_values(flat_values: NDArray[Any], mapping: ValueMapping) -> list[object]:
	"""
	Return the new value of each value of a flat Array, None for a missing one.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Keeps a value without ``ValueChange`` when ``others`` is ``Unmatched.KEEP``.

	Parameters
	----------
	flat_values
		The values of an Array in one dimension.
	mapping
		The new value of each listed value, and what happens to the others.

	Returns
	-------
	list[object]
		The new Python values, in order, a value without ``ValueChange`` kept as it is with ``Unmatched.KEEP``.

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

		if mapping.others == Unmatched.KEEP:
			new_values.append(value)
			continue

		new_values.append(None)

	return new_values


def find_result_type(array_type: Type, mapping: ValueMapping) -> Type:
	"""
	Return the type of the result of a mapping.

	Numbers given to an Array of numbers take its type, as with the operators, except decimals given to integers,
	which give ``FLOAT64``. Other new values give their own type, which also holds the kept values with
	``Unmatched.KEEP``. When every new value is None, the result keeps the type of the Array.

	.. versionadded:: 0.2.0

	Parameters
	----------
	array_type
		The type of the values of the Array.
	mapping
		The new value of each listed value, and what happens to the others.

	Returns
	-------
	Type
		The type holding every value of the result.

	Raises
	------
	IncompatibleTypesError
		When the kept values and the new values are of several families, such as numbers and texts.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.mapping.mapped_values import find_result_type
	>>> find_result_type(ndp.Type.INT8, ndp.ValueMapping(changes=[ndp.ValueChange(7, 70)]))
	<Type.INT8: 1>
	>>> find_result_type(ndp.Type.INT8, ndp.ValueMapping(changes=[ndp.ValueChange(7, 7.5)]))
	<Type.FLOAT64: 10>
	>>> find_result_type(ndp.Type.FLOAT32, ndp.ValueMapping(changes=[ndp.ValueChange(7, None)]))
	<Type.FLOAT32: 9>
	"""
	new_type = find_new_type(mapping.changes)
	if new_type is None:
		return array_type

	array_family = find_family(array_type)
	new_family = find_family(new_type)
	gives_numbers_to_numbers = array_family == ValueFamily.NUMBER and new_family == ValueFamily.NUMBER
	if gives_numbers_to_numbers:
		number_type = find_number_type(array_type, new_type)
		return number_type

	if mapping.others != Unmatched.KEEP:
		return new_type

	result_types = [array_type, new_type]
	result_type = find_common_type(result_types, MAPPING_OPERATION)

	return result_type


def find_number_type(array_type: Type, new_type: Type) -> Type:
	"""
	Return the type of Python numbers given to an Array of numbers.

	It is the type of the Array, as with the operators, except for decimals given to integers.

	.. versionadded:: 0.2.0

	Parameters
	----------
	array_type
		The number type of the Array.
	new_type
		``INT64`` for Python integers, ``FLOAT64`` when a Python decimal is among them.

	Returns
	-------
	Type
		``FLOAT64`` for decimals given to integers, which keeps the decimals as written, the type of the Array
		otherwise.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.mapping.mapped_values import find_number_type
	>>> find_number_type(ndp.Type.FLOAT32, ndp.Type.INT64), find_number_type(ndp.Type.UINT8, ndp.Type.FLOAT64)
	(<Type.FLOAT32: 9>, <Type.FLOAT64: 10>)
	"""
	gives_decimals_to_integers = new_type in DECIMAL_TYPES and array_type in INTEGER_TYPES
	if gives_decimals_to_integers:
		return Type.FLOAT64

	return array_type


def require_missing_supported(new_values: Sequence[object], new_type: Type, others: Unmatched) -> None:
	"""
	Check that a result of integers or booleans holds no missing value, with advice fitting a mapping.

	.. versionadded:: 0.1.0
	.. versionchanged:: 0.2.0
		Takes ``others``, which chooses the advice, and advises to convert the Array when every new value is None.

	Parameters
	----------
	new_values
		The new Python values, None for a missing one.
	new_type
		The type of the result.
	others
		What happens to a value without ``ValueChange``, which chooses the advice with the new values.

	Raises
	------
	UnsupportedMissingError
		When the type is an integer or boolean type and a new value is None.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.arrays.mapping.mapped_values import require_missing_supported
	>>> try:
	... 	require_missing_supported([10, None], ndp.Type.INT64, ndp.Unmatched.KEEP)
	... except ndp.UnsupportedMissingError as error:
	... 	print(error)
	INT64 values cannot be missing in an Array. Give decimal new values, such as 10.0,
	or convert the Array to FLOAT64 first.
	"""
	has_missing = None in new_values
	if not has_missing:
		return

	gives_only_missing = all(new_value is None for new_value in new_values)
	keeps_others = others == Unmatched.KEEP
	keeps_array_type = keeps_others or gives_only_missing
	if new_type in INTEGER_TYPES:
		integer_advice = KEPT_DECIMAL_ADVICE if keeps_array_type else DECIMAL_ADVICE
		raise UnsupportedMissingError(new_type.name, advice=integer_advice)

	if new_type == Type.BOOL:
		boolean_advice = KEPT_BOOLEAN_ADVICE if keeps_array_type else BOOLEAN_ADVICE
		raise UnsupportedMissingError(new_type.name, advice=boolean_advice)


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

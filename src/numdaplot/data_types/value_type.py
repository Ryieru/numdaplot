"""
Type of single Python values, and the common type of several values.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime, timedelta

import numpy

from numdaplot.data_types.library import Library
from numdaplot.data_types.type import Type
from numdaplot.data_types.value_family import find_family
from numdaplot.errors.incompatible_types_error import IncompatibleTypesError
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.errors.unsupported_type_error import UnsupportedTypeError

# bool comes before int and datetime before date, since each one is a subclass of the next.
PYTHON_TYPES = (
	((bool, numpy.bool_), Type.BOOL),
	((int, numpy.integer), Type.INT64),
	((float, numpy.floating), Type.FLOAT64),
	((str,), Type.TEXT),
	((datetime,), Type.DATETIME),
	((date,), Type.DATE),
	((timedelta,), Type.DURATION),
)
ARRAY_OPERATION = "An Array"
TYPE_WIDTHS = {
	Type.FLOAT64: 1,
	Type.DATETIME: 1,
}
NARROWEST_WIDTH = 0


def find_value_type(value: object) -> Type:
	"""
	Return the numdaplot type of a single Python value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		A boolean, a number, a text, a date, a datetime or a duration.

	Returns
	-------
	Type
		``BOOL``, ``INT64``, ``FLOAT64``, ``TEXT``, ``DATETIME``, ``DATE`` or ``DURATION``.

	Raises
	------
	UnsupportedTypeError
		When the value has no numdaplot type, such as a complex number or a tuple.
	TimeZoneMismatchError
		When the value is a datetime with a time zone, which an Array cannot hold.

	Examples
	--------
	>>> from numdaplot.data_types.value_type import find_value_type
	>>> find_value_type(2.5)
	<Type.FLOAT64: 10>
	"""
	has_time_zone = isinstance(value, datetime) and value.tzinfo is not None
	if has_time_zone:
		raise TimeZoneMismatchError(ARRAY_OPERATION, False)

	for python_types, data_type in PYTHON_TYPES:
		if isinstance(value, python_types):
			return data_type

	value_class = type(value)
	raise UnsupportedTypeError(value_class.__name__, Library.NUMPY)


def find_type_width(data_type: Type) -> int:
	"""
	Return the width of a type inside its family, the widest type holding every value of the others.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data_type
		A type returned by ``find_value_type``.

	Returns
	-------
	int
		1 for ``FLOAT64`` and ``DATETIME``, 0 for every other type.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.data_types.value_type import find_type_width
	>>> find_type_width(ndp.Type.INT64) < find_type_width(ndp.Type.FLOAT64)
	True
	"""
	width = TYPE_WIDTHS.get(data_type, NARROWEST_WIDTH)

	return width


def find_common_type(data_types: list[Type], operation: str) -> Type:
	"""
	Return the type that holds every value of several types of one family.

	Integers and decimals give ``FLOAT64``, dates and datetimes give ``DATETIME``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data_types
		At least one type returned by ``find_value_type``.
	operation
		Name of the operation needing the common type, shown in the error message.

	Returns
	-------
	Type
		The widest of the given types.

	Raises
	------
	IncompatibleTypesError
		When the types belong to several families, such as a number and a text.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.data_types.value_type import find_common_type
	>>> find_common_type([ndp.Type.INT64, ndp.Type.FLOAT64], "from_list")
	<Type.FLOAT64: 10>
	"""
	distinct_types = set(data_types)
	families = {find_family(data_type) for data_type in distinct_types}
	family_count = len(families)
	if family_count > 1:
		type_names = sorted(data_type.name for data_type in distinct_types)
		raise IncompatibleTypesError(operation, type_names)

	common_type = max(distinct_types, key=find_type_width)

	return common_type

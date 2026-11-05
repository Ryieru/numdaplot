"""
Conversion between ``ndp.Type`` and numpy dtypes, used by Array.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy

from numdaplot.data_types.library import Library
from numdaplot.data_types.type import Type
from numdaplot.errors.unsupported_type_error import UnsupportedTypeError

# Some versions of the numpy stubs leave out the missing value marker of StringDType.
STRING_DTYPE_CLASS = cast(Any, numpy.dtypes.StringDType)
TEXT_DTYPE = STRING_DTYPE_CLASS(na_object=numpy.nan)
NUMPY_DTYPE_CODES = {
	Type.INT8: "int8",
	Type.INT16: "int16",
	Type.INT32: "int32",
	Type.INT64: "int64",
	Type.UINT8: "uint8",
	Type.UINT16: "uint16",
	Type.UINT32: "uint32",
	Type.UINT64: "uint64",
	Type.FLOAT32: "float32",
	Type.FLOAT64: "float64",
	Type.BOOL: "bool",
	Type.DATE: "datetime64[D]",
	Type.DATETIME: "datetime64[ns]",
	Type.DURATION: "timedelta64[ns]",
}
NAMED_NUMPY_TYPES = (
	Type.INT8,
	Type.INT16,
	Type.INT32,
	Type.INT64,
	Type.UINT8,
	Type.UINT16,
	Type.UINT32,
	Type.UINT64,
	Type.FLOAT32,
	Type.FLOAT64,
	Type.BOOL,
)
TYPES_BY_DTYPE_NAME = {NUMPY_DTYPE_CODES[data_type]: data_type for data_type in NAMED_NUMPY_TYPES}
TEXT_KINDS = frozenset({"U", "T"})
DATETIME_KIND = "M"
DURATION_KIND = "m"
DAY_UNIT = "D"


def to_numpy_dtype(data_type: Type) -> numpy.dtype[Any]:
	"""
	Return the numpy dtype that stores the values of a numdaplot type.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data_type
		The numdaplot type to convert.

	Returns
	-------
	numpy.dtype
		The matching numpy dtype. ``TEXT`` gives the variable-length ``StringDType`` with NaN as missing value,
		``DATE`` gives ``datetime64[D]`` and ``DATETIME`` gives ``datetime64[ns]``.

	Raises
	------
	UnsupportedTypeError
		When the type has no numpy equivalent, which is the case of ``CATEGORY``.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.data_types.numpy_mapping import to_numpy_dtype
	>>> to_numpy_dtype(ndp.Type.INT32)
	dtype('int32')
	"""
	if data_type == Type.TEXT:
		return TEXT_DTYPE

	if data_type not in NUMPY_DTYPE_CODES:
		raise UnsupportedTypeError(data_type.name, Library.NUMPY)

	dtype_code = NUMPY_DTYPE_CODES[data_type]
	numpy_dtype = numpy.dtype(dtype_code)

	return numpy_dtype


def from_numpy_dtype(numpy_dtype: numpy.dtype[Any]) -> Type:
	"""
	Return the numdaplot type that matches a numpy dtype.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numpy_dtype
		The numpy dtype to convert. Fixed-length (``<U5``) and variable-length strings both give ``TEXT``,
		and every ``timedelta64`` unit gives ``DURATION``.

	Returns
	-------
	Type
		The matching numdaplot type.

	Raises
	------
	UnsupportedTypeError
		When numdaplot has no equivalent type, for example complex numbers or Python objects.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.data_types.numpy_mapping import from_numpy_dtype
	>>> from_numpy_dtype(numpy.dtype("datetime64[D]"))
	<Type.DATE: 14>
	"""
	dtype_name = numpy_dtype.name
	if dtype_name in TYPES_BY_DTYPE_NAME:
		named_type = TYPES_BY_DTYPE_NAME[dtype_name]
		return named_type

	dtype_kind = numpy_dtype.kind
	if dtype_kind in TEXT_KINDS:
		return Type.TEXT

	if dtype_kind == DURATION_KIND:
		return Type.DURATION

	if dtype_kind == DATETIME_KIND:
		datetime_type = find_datetime_type(numpy_dtype)
		return datetime_type

	type_name = str(numpy_dtype)
	raise UnsupportedTypeError(type_name, Library.NUMPY)


def find_datetime_type(numpy_dtype: numpy.dtype[Any]) -> Type:
	"""
	Return the numdaplot type of a ``datetime64`` dtype, according to its unit.

	.. versionadded:: 0.1.0

	Parameters
	----------
	numpy_dtype
		A ``datetime64`` dtype.

	Returns
	-------
	Type
		``DATE`` when the unit is the day, ``DATETIME`` for any other unit.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.data_types.numpy_mapping import find_datetime_type
	>>> find_datetime_type(numpy.dtype("datetime64[s]"))
	<Type.DATETIME: 15>
	"""
	datetime_unit, _ = numpy.datetime_data(numpy_dtype)
	if datetime_unit == DAY_UNIT:
		return Type.DATE

	return Type.DATETIME

"""
Conversion between ``ndp.Type`` and the pandas dtypes that store Table columns.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from pandas import DatetimeTZDtype
from pandas.api.extensions import ExtensionDtype
from pandas.api.types import pandas_dtype

from numdaplot.data_types.library import Library
from numdaplot.data_types.type import Type
from numdaplot.errors.unsupported_type_error import UnsupportedTypeError

PANDAS_DTYPE_CODES = {
	Type.INT8: "Int8",
	Type.INT16: "Int16",
	Type.INT32: "Int32",
	Type.INT64: "Int64",
	Type.UINT8: "UInt8",
	Type.UINT16: "UInt16",
	Type.UINT32: "UInt32",
	Type.UINT64: "UInt64",
	Type.FLOAT32: "float32",
	Type.FLOAT64: "float64",
	Type.BOOL: "boolean",
	Type.TEXT: "string",
	Type.CATEGORY: "category",
	Type.DATE: "datetime64[s]",
	Type.DATETIME: "datetime64[ns]",
	Type.DURATION: "timedelta64[ns]",
}
NANOSECOND_UNIT = "ns"
TYPES_BY_PANDAS_NAME = {dtype_code: data_type for data_type, dtype_code in PANDAS_DTYPE_CODES.items()}


def to_pandas_dtype(data_type: Type) -> numpy.dtype[Any] | ExtensionDtype:
	"""
	Return the pandas dtype that stores a Table column of a numdaplot type.

	Integers, booleans and text use the pandas types that accept missing values (``pd.NA``),
	so a column keeps its type when it has holes. Decimals keep NaN as missing value.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data_type
		The numdaplot type to convert.

	Returns
	-------
	numpy.dtype or ExtensionDtype
		The matching pandas dtype. ``DATE`` is stored as ``datetime64[s]``,
		since pandas has no dtype for a day without time.

	Examples
	--------
	>>> import numdaplot as ndp
	>>> from numdaplot.data_types.pandas_mapping import to_pandas_dtype
	>>> to_pandas_dtype(ndp.Type.INT64)
	Int64Dtype()
	"""
	dtype_code = PANDAS_DTYPE_CODES[data_type]
	matching_dtype = pandas_dtype(dtype_code)

	return matching_dtype


def from_pandas_dtype(pandas_type: object) -> Type:
	"""
	Return the numdaplot type of a Table column stored with a pandas dtype.

	.. versionadded:: 0.1.0

	Parameters
	----------
	pandas_type
		The dtype of a Table column, one of the dtypes given by ``to_pandas_dtype``.

	Returns
	-------
	Type
		The matching numdaplot type. Datetimes with a time zone, counted in nanoseconds, give ``DATETIME``.

	Raises
	------
	UnsupportedTypeError
		When the dtype is not one that stores a Table column, such as ``object`` or ``complex128``.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.data_types.pandas_mapping import from_pandas_dtype
	>>> from_pandas_dtype(pandas.Int64Dtype())
	<Type.INT64: 4>
	>>> from_pandas_dtype(pandas.DatetimeTZDtype("ns", "Europe/Paris"))
	<Type.DATETIME: 15>
	"""
	is_nanosecond_zone = isinstance(pandas_type, DatetimeTZDtype) and pandas_type.unit == NANOSECOND_UNIT
	if is_nanosecond_zone:
		return Type.DATETIME

	dtype_name = str(pandas_type)
	if dtype_name not in TYPES_BY_PANDAS_NAME:
		raise UnsupportedTypeError(dtype_name, Library.PANDAS)

	matching_type = TYPES_BY_PANDAS_NAME[dtype_name]

	return matching_type

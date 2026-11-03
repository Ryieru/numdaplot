"""
Conversion from ``ndp.Type`` to pandas dtypes, used by Table.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from pandas.api.extensions import ExtensionDtype
from pandas.api.types import pandas_dtype

from numdaplot.data_types.type import Type

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

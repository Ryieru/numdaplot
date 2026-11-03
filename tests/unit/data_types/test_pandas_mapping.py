"""
Unit tests of the conversion from ndp.Type to pandas dtypes.

.. versionadded:: 0.1.0
"""

import numpy
import pandas
import pytest

from numdaplot.data_types.pandas_mapping import to_pandas_dtype
from numdaplot.data_types.type import Type

NULLABLE_TYPES = [
	Type.INT8,
	Type.INT16,
	Type.INT32,
	Type.INT64,
	Type.UINT8,
	Type.UINT16,
	Type.UINT32,
	Type.UINT64,
	Type.BOOL,
	Type.TEXT,
]
SAMPLE_SIZE = 2


def test_to_pandas_dtype_converts_int64_to_nullable_integers() -> None:
	"""
	Check that INT64 gives the pandas Int64 dtype, which accepts missing values.

	.. versionadded:: 0.1.0
	"""
	pandas_dtype = to_pandas_dtype(Type.INT64)

	expected_dtype = pandas.Int64Dtype()
	assert pandas_dtype == expected_dtype


def test_to_pandas_dtype_keeps_numpy_float64_for_decimals() -> None:
	"""
	Check that FLOAT64 gives the numpy float64 dtype, which keeps NaN as missing value.

	.. versionadded:: 0.1.0
	"""
	pandas_dtype = to_pandas_dtype(Type.FLOAT64)

	expected_dtype = numpy.dtype(numpy.float64)
	assert pandas_dtype == expected_dtype


def test_to_pandas_dtype_converts_category() -> None:
	"""
	Check that CATEGORY gives the pandas categorical dtype.

	.. versionadded:: 0.1.0
	"""
	pandas_dtype = to_pandas_dtype(Type.CATEGORY)

	assert isinstance(pandas_dtype, pandas.CategoricalDtype)


@pytest.mark.parametrize("data_type", NULLABLE_TYPES)
def test_to_pandas_dtype_keeps_the_type_of_a_column_with_a_hole(data_type: Type) -> None:
	"""
	Check that a column of integers, booleans or texts keeps its dtype when a value is missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data_type
		A type stored with a pandas dtype that accepts missing values.
	"""
	pandas_dtype = to_pandas_dtype(data_type)
	missing_values = [pandas.NA] * SAMPLE_SIZE
	column = pandas.Series(missing_values, dtype=pandas_dtype)

	assert column.dtype == pandas_dtype


@pytest.mark.parametrize("data_type", list(Type))
def test_to_pandas_dtype_converts_every_type(data_type: Type) -> None:
	"""
	Check that every numdaplot type has a pandas dtype that pandas accepts for a column.

	The dtype names are compared, because a category column holds its own list of categories
	while the generic category dtype has none.

	.. versionadded:: 0.1.0

	Parameters
	----------
	data_type
		Any numdaplot type.
	"""
	pandas_dtype = to_pandas_dtype(data_type)
	column = pandas.Series([], dtype=pandas_dtype)

	assert column.dtype.name == pandas_dtype.name

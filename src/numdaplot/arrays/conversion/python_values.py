"""
Conversion of the values of an Array to Python values.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

from numpy.typing import NDArray

from numdaplot.data_types.numpy_mapping import from_numpy_dtype
from numdaplot.data_types.type import Type

# Python datetimes and timedeltas stop at the microsecond; finer numpy units would become integers.
PYTHON_TIME_DTYPES = {
	Type.DATETIME: "datetime64[us]",
	Type.DURATION: "timedelta64[us]",
}


def to_python_list(values: NDArray[Any]) -> list[Any]:
	"""
	Return the values as Python values, in nested lists for several dimensions.

	Datetimes become ``datetime``, dates ``date``, durations ``timedelta``, and a missing date,
	datetime or duration becomes ``None``. A missing decimal stays ``nan``.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		The values of an Array.

	Returns
	-------
	list[Any]
		The Python values, one nested list per dimension after the first.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.conversion.python_values import to_python_list
	>>> to_python_list(numpy.array(["2026-01-31T08:30", "NaT"], dtype="datetime64[ns]"))
	[datetime.datetime(2026, 1, 31, 8, 30), None]
	"""
	array_type = from_numpy_dtype(values.dtype)
	converted_values = values
	if array_type in PYTHON_TIME_DTYPES:
		python_time_dtype = PYTHON_TIME_DTYPES[array_type]
		converted_values = values.astype(python_time_dtype)

	raw_values = converted_values.tolist()
	python_values = cast(list[Any], raw_values)

	return python_values

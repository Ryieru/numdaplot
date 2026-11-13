"""
Conversion of numpy arrays to the values stored by an Array.

.. versionadded:: 0.1.0
"""

from typing import Any

import numpy
from numpy.typing import NDArray

from numdaplot.errors.time_overflow_error import TimeOverflowError
from numdaplot.types.numpy_mapping import from_numpy_dtype, to_numpy_dtype
from numdaplot.types.time_of_day import TIME_DTYPE, holds_only_times, store_time_objects
from numdaplot.types.type import Type

TEXT_KINDS = frozenset({"U", "T"})
NANOSECOND_DURATION_DTYPE = numpy.dtype("timedelta64[ns]")
FROM_NUMPY_OPERATION = "from_numpy"


def copy_numpy_values(values: NDArray[Any]) -> NDArray[Any]:
	"""
	Return a copy of a numpy array that an Array can store.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		A numpy array of a type numdaplot supports.

	Returns
	-------
	NDArray
		An independent copy, with texts stored as variable-length texts with NaN as missing value. An object
		array of Python times of day gives times of day, and durations in microseconds give nanoseconds, as
		microseconds store the times of day.

	Raises
	------
	UnsupportedTypeError
		When numdaplot has no equivalent type, for example complex numbers or other Python objects.
	TimeOverflowError
		When a duration in microseconds is beyond about 292 years, which nanoseconds cannot hold.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.creation.numpy_conversion import copy_numpy_values
	>>> copy_numpy_values(numpy.array(["a", "bc"])).dtype
	StringDType(na_object=nan)
	"""
	if holds_only_times(values):
		time_values = store_time_objects(values)
		return time_values

	from_numpy_dtype(values.dtype)
	copied_values = values.copy()
	duration_values = normalize_durations(copied_values)
	normalized_values = normalize_text(duration_values)

	return normalized_values


def normalize_text(values: NDArray[Any]) -> NDArray[Any]:
	"""
	Return values whose texts are stored with the numpy type of every ``TEXT`` Array.

	Fixed-length texts become variable-length texts, and any other marker of a missing text becomes NaN.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		A numpy array of any type.

	Returns
	-------
	NDArray
		The same array when it holds no text or already has this type, otherwise a converted copy.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.creation.numpy_conversion import normalize_text
	>>> normalize_text(numpy.array(["a"])).dtype
	StringDType(na_object=nan)
	>>> marked_with_none = numpy.dtypes.StringDType(na_object=None)
	>>> normalize_text(numpy.array(["a", None], dtype=marked_with_none))
	array(['a', nan], dtype=StringDType(na_object=nan))
	"""
	if values.dtype.kind not in TEXT_KINDS:
		return values

	text_dtype = to_numpy_dtype(Type.TEXT)
	if values.dtype == text_dtype:
		return values

	text_values = values.astype(text_dtype)

	return text_values


def normalize_durations(values: NDArray[Any]) -> NDArray[Any]:
	"""
	Return durations in microseconds as nanoseconds, since microseconds store the times of day.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		A numpy array of any type.

	Returns
	-------
	NDArray
		The same array unless it holds durations in microseconds, which become nanoseconds.

	Raises
	------
	TimeOverflowError
		When a duration is beyond about 292 years, which nanoseconds cannot hold.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.arrays.creation.numpy_conversion import normalize_durations
	>>> normalize_durations(numpy.array([1, "NaT"], dtype="timedelta64[us]"))
	array([ 1000, 'NaT'], dtype='timedelta64[ns]')
	"""
	if values.dtype != TIME_DTYPE:
		return values

	try:
		nanosecond_values = values.astype(NANOSECOND_DURATION_DTYPE)
	except OverflowError as error:
		raise TimeOverflowError(FROM_NUMPY_OPERATION, Type.DURATION.name) from error

	# Some versions of numpy wrap a value beyond the range of nanoseconds instead of raising.
	microsecond_values = nanosecond_values.astype(TIME_DTYPE)
	is_kept = (microsecond_values == values) | numpy.isnat(values)
	is_exact = bool(is_kept.all())
	if not is_exact:
		raise TimeOverflowError(FROM_NUMPY_OPERATION, Type.DURATION.name)

	return nanosecond_values

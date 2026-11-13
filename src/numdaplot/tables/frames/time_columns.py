"""
Table columns of times of day, and the durations a Table reads from outside numdaplot.

.. versionadded:: 0.1.0
"""

from typing import Any, cast

import numpy
import pandas
from numpy.typing import NDArray

from numdaplot.arrays.conversion.time_text import format_times
from numdaplot.tables.frames.column import Column
from numdaplot.tables.frames.time_range_errors import TimeRangeErrors
from numdaplot.types.time_of_day import TIME_DTYPE, read_time_objects, store_time_objects

DURATION_KIND = "m"
NANOSECOND_DURATION_DTYPE = numpy.dtype("timedelta64[ns]")
PYTHON_OBJECT_DTYPE = numpy.dtype(object)
TEXT_PANDAS_DTYPE = "string"
TABLE_CREATION_OPERATION = "Table creation"


def is_time_column(column: Column) -> bool:
	"""
	Return whether a Table column stores times of day.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column.

	Returns
	-------
	bool
		True for a column in ``timedelta64[us]``.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.time_columns import is_time_column
	>>> import numpy
	>>> is_time_column(pandas.Series(numpy.array([1], dtype="timedelta64[us]"))), is_time_column(pandas.Series([1]))
	(True, False)
	"""
	holds_times = column.dtype == TIME_DTYPE

	return holds_times


def read_time_objects_column(column: Column) -> Column:
	"""
	Return a column of times of day as Python ``datetime.time`` objects, None where missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column of times of day.

	Returns
	-------
	Column
		An object column with the same index.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.time_columns import read_time_objects_column
	>>> import numpy
	>>> minutes = pandas.Series(numpy.array([60000000], dtype="timedelta64[us]"))
	>>> read_time_objects_column(minutes).tolist()
	[datetime.time(0, 1)]
	"""
	stored_times = column.to_numpy(dtype=TIME_DTYPE)
	time_objects = read_time_objects(stored_times)
	object_column = pandas.Series(time_objects, index=column.index, name=column.name, dtype=PYTHON_OBJECT_DTYPE)

	return object_column


def store_time_column(column: Column) -> Column:
	"""
	Return a column of Python times of day stored as the time since midnight.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		An object column of ``datetime.time`` and missing values.

	Returns
	-------
	Column
		A column in ``timedelta64[us]`` with the same index, NaT where missing.

	Examples
	--------
	>>> from datetime import time
	>>> import pandas
	>>> from numdaplot.tables.frames.time_columns import store_time_column
	>>> store_time_column(pandas.Series([time(0, 1), None], dtype=object)).tolist()
	[Timedelta('0 days 00:01:00'), NaT]
	"""
	object_values = read_object_values(column)
	stored_times = store_time_objects(object_values)
	time_column = pandas.Series(stored_times, index=column.index, name=column.name)

	return time_column


def read_object_values(column: Column) -> NDArray[Any]:
	"""
	Return the values of a column as Python objects, None where missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A column of any dtype.

	Returns
	-------
	NDArray
		An object array, None for every missing marker such as NaN or ``pd.NA``.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.time_columns import read_object_values
	>>> read_object_values(pandas.Series(["a", float("nan")], dtype=object))
	array(['a', None], dtype=object)
	"""
	missing = column.isna()
	missing_flags = missing.to_numpy(dtype=bool)
	# Some versions of the numpy stubs refuse None as a value of an object array.
	object_values = cast(Any, column.to_numpy(dtype=PYTHON_OBJECT_DTYPE, copy=True))
	object_values[missing_flags] = None

	return object_values


def convert_outside_durations(frame: pandas.DataFrame) -> pandas.DataFrame:
	"""
	Return a DataFrame read from outside numdaplot whose durations, of any unit, are stored in nanoseconds.

	Microseconds store the times of day, so an outside duration in microseconds must not keep them.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		A DataFrame read from a file or given by the user. It is not changed.

	Returns
	-------
	pandas.DataFrame
		The DataFrame, a copy with its duration columns in ``timedelta64[ns]`` when it has some.

	Raises
	------
	TimeOverflowError
		When a duration is beyond about 292 years, which nanoseconds cannot hold.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.time_columns import convert_outside_durations
	>>> import numpy
	>>> frame = pandas.DataFrame({"wait": numpy.array([5], dtype="timedelta64[us]")})
	>>> convert_outside_durations(frame).dtypes.tolist()
	[dtype('<m8[ns]')]
	"""
	duration_names = [name for name in frame.columns if frame[name].dtype.kind == DURATION_KIND]
	if duration_names == []:
		return frame

	converted_frame = frame.copy(deep=False)
	for column_name in duration_names:
		column = frame[column_name]
		duration_values = column.to_numpy()
		nanosecond_values = convert_to_nanoseconds(duration_values, str(column_name))
		nanosecond_column = pandas.Series(nanosecond_values, index=column.index, name=column.name)
		converted_frame[column_name] = nanosecond_column

	return converted_frame


def convert_to_nanoseconds(durations: NDArray[Any], column_name: str) -> NDArray[Any]:
	"""
	Return durations of any unit in nanoseconds, refusing those that nanoseconds cannot hold.

	.. versionadded:: 0.1.0

	Parameters
	----------
	durations
		Durations in ``timedelta64`` of any unit.
	column_name
		The name of the column holding them, named by the error.

	Returns
	-------
	NDArray
		The durations in ``timedelta64[ns]``.

	Raises
	------
	TimeOverflowError
		When a duration is beyond about 292 years.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.tables.frames.time_columns import convert_to_nanoseconds
	>>> convert_to_nanoseconds(numpy.array([2], dtype="timedelta64[s]"), "wait")
	array([2000000000], dtype='timedelta64[ns]')
	"""
	with TimeRangeErrors(TABLE_CREATION_OPERATION, column_name):
		try:
			nanosecond_values = durations.astype(NANOSECOND_DURATION_DTYPE)
		except OverflowError as error:
			raise pandas.errors.OutOfBoundsTimedelta from error

		# Some versions of numpy wrap a duration beyond the range of nanoseconds instead of raising.
		original_values = nanosecond_values.astype(durations.dtype)
		is_kept = (original_values == durations) | numpy.isnat(durations)
		is_exact = bool(is_kept.all())
		if not is_exact:
			raise pandas.errors.OutOfBoundsTimedelta

	return nanosecond_values


def read_time_objects_frame(frame: pandas.DataFrame) -> pandas.DataFrame:
	"""
	Return a DataFrame whose columns of times of day hold Python ``datetime.time`` objects.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table. It is not changed.

	Returns
	-------
	pandas.DataFrame
		A deep copy, each column of times of day as an object column.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.time_columns import read_time_objects_frame
	>>> import numpy
	>>> frame = pandas.DataFrame({"hour": numpy.array([60000000], dtype="timedelta64[us]")})
	>>> read_time_objects_frame(frame)["hour"].tolist()
	[datetime.time(0, 1)]
	"""
	frame_copy = frame.copy(deep=True)
	for column_name in frame.columns:
		column = frame[column_name]
		if is_time_column(column):
			object_column = read_time_objects_column(column)
			frame_copy[column_name] = object_column

	return frame_copy


def write_time_texts_column(column: Column) -> Column:
	"""
	Return a column of times of day as texts, such as ``15:35:00``, ``NaT`` where missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	column
		A Table column of times of day.

	Returns
	-------
	Column
		An object column of texts with the same index.

	Examples
	--------
	>>> import pandas
	>>> from numdaplot.tables.frames.time_columns import write_time_texts_column
	>>> import numpy
	>>> hours = pandas.Series(numpy.array([56100000000, "NaT"], dtype="timedelta64[us]"))
	>>> write_time_texts_column(hours).tolist()
	['15:35:00', 'NaT']
	"""
	stored_times = column.to_numpy(dtype=TIME_DTYPE)
	time_texts = format_times(stored_times)
	text_column = pandas.Series(time_texts, index=column.index, name=column.name, dtype=PYTHON_OBJECT_DTYPE)

	return text_column


def write_time_texts_frame(frame: pandas.DataFrame) -> pandas.DataFrame:
	"""
	Return a DataFrame whose columns of times of day are written as texts, missing where a time is missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	frame
		The columns of a Table. It is not changed.

	Returns
	-------
	pandas.DataFrame
		A copy, each column of times of day as texts such as ``15:35:00``.

	Examples
	--------
	>>> import numpy
	>>> import pandas
	>>> from numdaplot.tables.frames.time_columns import write_time_texts_frame
	>>> frame = pandas.DataFrame({"hour": numpy.array([56100000000, "NaT"], dtype="timedelta64[us]")})
	>>> write_time_texts_frame(frame)["hour"].tolist()
	['15:35:00', <NA>]
	"""
	text_frame = frame.copy()
	for column_name in frame.columns:
		column = frame[column_name]
		if is_time_column(column):
			time_texts = write_time_texts_column(column)
			missing = column.isna()
			# Some versions of the pandas stubs leave the types of mask partly unknown.
			text_column = cast(Any, time_texts)
			present_texts = cast(Column, text_column.mask(missing))
			text_frame[column_name] = present_texts.astype(TEXT_PANDAS_DTYPE)

	return text_frame

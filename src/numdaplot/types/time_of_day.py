"""
Conversion between Python times of day and the time since midnight that stores them.

.. versionadded:: 0.1.0
"""

from collections.abc import Sequence
from datetime import time, timedelta
from typing import Any, cast

import numpy
from numpy.typing import NDArray

TIME_DTYPE = numpy.dtype("timedelta64[us]")
PYTHON_OBJECT_DTYPE = numpy.dtype(object)
MISSING_TIME = numpy.timedelta64("NaT", "us")
MICROSECONDS_PER_SECOND = 1_000_000
SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60


def to_time_since_midnight(time_of_day: time) -> timedelta:
	"""
	Return the time elapsed since midnight at a time of day.

	.. versionadded:: 0.1.0

	Parameters
	----------
	time_of_day
		A time without time zone.

	Returns
	-------
	timedelta
		The duration from midnight to the time.

	Examples
	--------
	>>> from datetime import time
	>>> from numdaplot.types.time_of_day import to_time_since_midnight
	>>> to_time_since_midnight(time(15, 35, 0, 250000))
	datetime.timedelta(seconds=56100, microseconds=250000)
	"""
	since_midnight = timedelta(
		hours=time_of_day.hour,
		minutes=time_of_day.minute,
		seconds=time_of_day.second,
		microseconds=time_of_day.microsecond,
	)

	return since_midnight


def to_time_of_day(microseconds: int) -> time:
	"""
	Return the time of day reached a number of microseconds after midnight.

	.. versionadded:: 0.1.0

	Parameters
	----------
	microseconds
		The microseconds since midnight, less than one day.

	Returns
	-------
	time
		The time of day.

	Examples
	--------
	>>> from numdaplot.types.time_of_day import to_time_of_day
	>>> to_time_of_day(56100250000)
	datetime.time(15, 35, 0, 250000)
	"""
	total_seconds, microsecond = divmod(microseconds, MICROSECONDS_PER_SECOND)
	total_minutes, second = divmod(total_seconds, SECONDS_PER_MINUTE)
	hour, minute = divmod(total_minutes, MINUTES_PER_HOUR)
	time_of_day = time(hour, minute, second, microsecond)

	return time_of_day


def store_times(times: Sequence[object]) -> NDArray[numpy.timedelta64]:
	"""
	Return times of day as the time since midnight in microseconds, NaT where missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	times
		Python times of day, and None or NaT for a missing value.

	Returns
	-------
	NDArray[numpy.timedelta64]
		The values in ``timedelta64[us]``.

	Examples
	--------
	>>> from datetime import time
	>>> from numdaplot.types.time_of_day import store_times
	>>> store_times([time(0, 0, 1), None])
	array([1000000,     'NaT'], dtype='timedelta64[us]')
	"""
	durations = list[object]()
	for value in times:
		duration: object = MISSING_TIME
		if isinstance(value, time):
			duration = to_time_since_midnight(value)

		durations.append(duration)

	stored_times = numpy.array(durations, dtype=TIME_DTYPE)

	return stored_times


def read_times(values: NDArray[Any]) -> list[time | None]:
	"""
	Return the Python times of day of values stored as the time since midnight, None where missing.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Values in ``timedelta64[us]``, in one dimension.

	Returns
	-------
	list[time | None]
		One time of day per value.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.types.time_of_day import read_times
	>>> read_times(numpy.array([56100000000, "NaT"], dtype="timedelta64[us]"))
	[datetime.time(15, 35), None]
	"""
	missing = numpy.isnat(values)
	missing_flags = cast(list[bool], missing.tolist())
	whole_values = values.astype(numpy.int64)
	microsecond_list = cast(list[int], whole_values.tolist())
	times = list[time | None]()
	for microseconds, is_missing in zip(microsecond_list, missing_flags, strict=True):
		if is_missing:
			times.append(None)
			continue

		time_of_day = to_time_of_day(microseconds)
		times.append(time_of_day)

	return times


def write_time(time_of_day: time) -> str:
	"""
	Return a time of day as a text, with its microseconds only when it has some.

	.. versionadded:: 0.1.0

	Parameters
	----------
	time_of_day
		A time of day.

	Returns
	-------
	str
		``15:35:00``, or ``15:35:00.250000`` with microseconds.

	Examples
	--------
	>>> from datetime import time
	>>> from numdaplot.types.time_of_day import write_time
	>>> write_time(time(15, 35)), write_time(time(15, 35, 0, 250000))
	('15:35:00', '15:35:00.250000')
	"""
	time_text = time_of_day.isoformat()

	return time_text


def read_time_objects(values: NDArray[Any]) -> NDArray[Any]:
	"""
	Return values stored as the time since midnight as Python times of day, in the same shape.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		Values in ``timedelta64[us]``, of any shape.

	Returns
	-------
	NDArray
		An object array of ``datetime.time``, None where missing.

	Examples
	--------
	>>> import numpy
	>>> from numdaplot.types.time_of_day import read_time_objects
	>>> read_time_objects(numpy.array([[60000000]], dtype="timedelta64[us]"))
	array([[datetime.time(0, 1)]], dtype=object)
	"""
	flat_values = values.ravel()
	times = read_times(flat_values)
	time_count = len(times)
	# Some versions of the numpy stubs refuse Python objects as the values of an object array.
	time_objects = cast(Any, numpy.empty(time_count, dtype=PYTHON_OBJECT_DTYPE))
	time_objects[:] = times
	shaped_objects = time_objects.reshape(values.shape)

	return shaped_objects


def holds_only_times(values: NDArray[Any]) -> bool:
	"""
	Return whether an object array holds Python times of day and missing values only, with at least one time.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		A numpy array of any type.

	Returns
	-------
	bool
		True for an object array of ``datetime.time`` without time zone and None.

	Examples
	--------
	>>> from datetime import time
	>>> import numpy
	>>> from numdaplot.types.time_of_day import holds_only_times
	>>> holds_only_times(numpy.array([time(8), None], dtype=object)), holds_only_times(numpy.array([1, 2]))
	(True, False)
	"""
	if values.dtype != PYTHON_OBJECT_DTYPE:
		return False

	has_time = False
	for value in values.ravel():
		if value is None:
			continue

		is_naive_time = isinstance(value, time) and value.tzinfo is None
		if not is_naive_time:
			return False

		has_time = True

	return has_time


def store_time_objects(values: NDArray[Any]) -> NDArray[numpy.timedelta64]:
	"""
	Return an object array of Python times of day as the time since midnight, in the same shape.

	.. versionadded:: 0.1.0

	Parameters
	----------
	values
		An object array of ``datetime.time`` and None.

	Returns
	-------
	NDArray[numpy.timedelta64]
		The values in ``timedelta64[us]``, NaT where missing.

	Examples
	--------
	>>> from datetime import time
	>>> import numpy
	>>> from numdaplot.types.time_of_day import store_time_objects
	>>> store_time_objects(numpy.array([time(0, 0, 1), None], dtype=object))
	array([1000000,     'NaT'], dtype='timedelta64[us]')
	"""
	flat_values = values.ravel()
	value_list = flat_values.tolist()
	stored_times = store_times(value_list)
	shaped_times = stored_times.reshape(values.shape)

	return shaped_times

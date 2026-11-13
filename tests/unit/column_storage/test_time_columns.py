"""
Unit tests of the Table columns of times of day and of the durations read from outside numdaplot.

.. versionadded:: 0.1.0
"""

from datetime import time
from typing import Any

import numpy
import pandas
import pytest

from numdaplot.column_storage.time_columns import (
	convert_outside_durations,
	convert_to_nanoseconds,
	is_time_column,
	read_object_values,
	read_time_objects_column,
	read_time_objects_frame,
	store_time_column,
	write_time_texts_column,
	write_time_texts_frame,
)
from numdaplot.errors.time_overflow_error import TimeOverflowError

TIME_COLUMN = pandas.Series(numpy.array([56100000000, "NaT"], dtype="timedelta64[us]"))
NANOSECOND_COLUMN = pandas.Series(numpy.array([1], dtype="timedelta64[ns]"))
EXPECTED_TIMES = [time(15, 35), None]
OBJECT_TIMES = pandas.Series([time(15, 35), numpy.nan], dtype=object)
TIME_DTYPE_NAME = "timedelta64[us]"
EXPECTED_MISSING = [False, True]
EXPECTED_TEXTS = ["15:35:00", "NaT"]
EXPECTED_HOUR_TEXTS = ["15:35:00", pandas.NA]
MIXED_OBJECTS = pandas.Series(["a", float("nan"), pandas.NA], dtype=object)
EXPECTED_OBJECTS = ["a", None, None]
MICROSECOND_FRAME = pandas.DataFrame({"wait": pandas.Series(numpy.array([5], dtype="timedelta64[us]")), "count": [1]})
NANOSECOND_DTYPE_NAME = "timedelta64[ns]"
FAR_FRAME = pandas.DataFrame({"wait": pandas.Series(numpy.array([2**62], dtype="timedelta64[us]"))})
COUNT_FRAME = pandas.DataFrame({"count": [1]})
WAIT_COLUMN = "wait"
TIME_AND_WAIT = pandas.DataFrame(
	{"hour": TIME_COLUMN, "wait": pandas.Series(numpy.array([1, 2], dtype="timedelta64[ns]"))}
)


def test_is_time_column_recognizes_microseconds_only() -> None:
	"""
	Check a column of times and a column of durations.

	.. versionadded:: 0.1.0
	"""
	is_time = is_time_column(TIME_COLUMN)
	is_duration_time = is_time_column(NANOSECOND_COLUMN)

	assert is_time
	assert not is_duration_time


def test_read_time_objects_column_gives_python_times() -> None:
	"""
	Check the objects of a column of times.

	.. versionadded:: 0.1.0
	"""
	object_column = read_time_objects_column(TIME_COLUMN)

	times = object_column.tolist()
	assert times == EXPECTED_TIMES


def test_store_time_column_reads_nan_as_missing() -> None:
	"""
	Check that Python times with NaN give a column of times with NaT.

	.. versionadded:: 0.1.0
	"""
	time_column = store_time_column(OBJECT_TIMES)

	dtype_name = str(time_column.dtype)
	missing = time_column.isna()
	missing_list = missing.tolist()
	assert dtype_name == TIME_DTYPE_NAME
	assert missing_list == EXPECTED_MISSING


def test_read_object_values_gives_none_for_every_missing_marker() -> None:
	"""
	Check NaN and pd.NA.

	.. versionadded:: 0.1.0
	"""
	object_values = read_object_values(MIXED_OBJECTS)

	value_list = object_values.tolist()
	assert value_list == EXPECTED_OBJECTS


def test_convert_outside_durations_stores_nanoseconds() -> None:
	"""
	Check that an outside duration in microseconds becomes nanoseconds, other columns kept.

	.. versionadded:: 0.1.0
	"""
	converted_frame = convert_outside_durations(MICROSECOND_FRAME)

	wait_column = converted_frame["wait"]
	wait_dtype = str(wait_column.dtype)
	assert wait_dtype == NANOSECOND_DTYPE_NAME


def test_convert_outside_durations_keeps_a_frame_without_duration() -> None:
	"""
	Check that a DataFrame without duration is given back.

	.. versionadded:: 0.1.0
	"""
	converted_frame = convert_outside_durations(COUNT_FRAME)

	assert converted_frame is COUNT_FRAME


def test_convert_outside_durations_rejects_a_duration_beyond_nanoseconds() -> None:
	"""
	Check that a duration too long for nanoseconds raises TimeOverflowError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(TimeOverflowError):
		convert_outside_durations(FAR_FRAME)


def test_convert_to_nanoseconds_rejects_a_duration_numpy_cannot_convert(overflowing_durations: Any) -> None:
	"""
	Check that a numpy raising OverflowError for nanoseconds gives TimeOverflowError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	overflowing_durations
		Durations whose conversion raises.
	"""
	with pytest.raises(TimeOverflowError):
		convert_to_nanoseconds(overflowing_durations, WAIT_COLUMN)


def test_convert_to_nanoseconds_rejects_a_duration_numpy_wraps_around(wrapping_durations: Any) -> None:
	"""
	Check that a numpy wrapping the value around for nanoseconds gives TimeOverflowError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	wrapping_durations
		Durations whose conversion wraps around.
	"""
	with pytest.raises(TimeOverflowError):
		convert_to_nanoseconds(wrapping_durations, WAIT_COLUMN)


def test_read_time_objects_frame_turns_only_times_into_objects() -> None:
	"""
	Check a DataFrame of a column of times and a column of durations.

	.. versionadded:: 0.1.0
	"""
	object_frame = read_time_objects_frame(TIME_AND_WAIT)

	hour_column = object_frame["hour"]
	wait_column = object_frame["wait"]
	hours = hour_column.tolist()
	wait_dtype = str(wait_column.dtype)
	assert hours == EXPECTED_TIMES
	assert wait_dtype == NANOSECOND_DTYPE_NAME


def test_write_time_texts_column_writes_times_and_nat() -> None:
	"""
	Check the texts shown for a column of times.

	.. versionadded:: 0.1.0
	"""
	text_column = write_time_texts_column(TIME_COLUMN)

	texts = text_column.tolist()
	assert texts == EXPECTED_TEXTS


def test_write_time_texts_frame_writes_only_times_as_texts() -> None:
	"""
	Check that a column of times becomes texts, missing kept, and a column of durations stays.

	.. versionadded:: 0.1.0
	"""
	text_frame = write_time_texts_frame(TIME_AND_WAIT)

	hour_column = text_frame["hour"]
	wait_column = text_frame["wait"]
	hours = hour_column.tolist()
	wait_dtype = str(wait_column.dtype)
	assert hours == EXPECTED_HOUR_TEXTS
	assert wait_dtype == NANOSECOND_DTYPE_NAME

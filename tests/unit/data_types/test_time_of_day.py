"""
Unit tests of the conversion between Python times of day and their storage.

.. versionadded:: 0.1.0
"""

from datetime import UTC, time, timedelta

import numpy

from numdaplot.data_types.time_of_day import (
	TIME_DTYPE,
	holds_only_times,
	read_time_objects,
	read_times,
	store_time_objects,
	store_times,
	to_time_of_day,
	to_time_since_midnight,
	write_time,
)

AFTERNOON = time(15, 35, 0, 250000)
AFTERNOON_DURATION = timedelta(hours=15, minutes=35, microseconds=250000)
AFTERNOON_MICROSECONDS = 56100250000
LAST_TIME = time(23, 59, 59, 999999)
LAST_MICROSECONDS = 86399999999
TIMES = [time(0, 1), None]
STORED_TIMES = numpy.array([60000000, "NaT"], dtype=TIME_DTYPE)
EXPECTED_TIMES = [time(0, 1), None]
GRID = numpy.array([[60000000, "NaT"]], dtype=TIME_DTYPE)
OBJECT_TIMES = numpy.array([time(8), None], dtype=object)
ZONED_TIMES = numpy.array([time(8, tzinfo=UTC)], dtype=object)
MIXED_OBJECTS = numpy.array([time(8), "08:00"], dtype=object)
ONLY_MISSING = numpy.array([None], dtype=object)
INTEGERS = numpy.array([1, 2])
EXPECTED_SHORT_TEXT = "15:35:00"
SHORT_AFTERNOON = time(15, 35)
EXPECTED_MISSING = [False, True]
EXPECTED_GRID_TIMES = [[time(0, 1), None]]
EXPECTED_LONG_TEXT = "15:35:00.250000"


def test_to_time_since_midnight_counts_every_part() -> None:
	"""
	Check hours, minutes, seconds and microseconds.

	.. versionadded:: 0.1.0
	"""
	since_midnight = to_time_since_midnight(AFTERNOON)

	assert since_midnight == AFTERNOON_DURATION


def test_to_time_of_day_gives_back_the_time() -> None:
	"""
	Check the reverse conversion, up to the last microsecond of the day.

	.. versionadded:: 0.1.0
	"""
	afternoon = to_time_of_day(AFTERNOON_MICROSECONDS)
	last_time = to_time_of_day(LAST_MICROSECONDS)

	assert afternoon == AFTERNOON
	assert last_time == LAST_TIME


def test_store_times_stores_microseconds_and_missing_values() -> None:
	"""
	Check the dtype and NaT for None.

	.. versionadded:: 0.1.0
	"""
	stored_times = store_times(TIMES)

	missing = numpy.isnat(stored_times)
	missing_list = missing.tolist()
	assert stored_times.dtype == TIME_DTYPE
	assert missing_list == EXPECTED_MISSING


def test_read_times_gives_python_times_and_none() -> None:
	"""
	Check the times read from storage.

	.. versionadded:: 0.1.0
	"""
	times = read_times(STORED_TIMES)

	assert times == EXPECTED_TIMES


def test_read_time_objects_keeps_the_shape() -> None:
	"""
	Check an object array of the same shape.

	.. versionadded:: 0.1.0
	"""
	time_objects = read_time_objects(GRID)

	object_list = time_objects.tolist()
	assert time_objects.shape == GRID.shape
	assert object_list == EXPECTED_GRID_TIMES


def test_holds_only_times_accepts_times_and_none() -> None:
	"""
	Check an object array of times with a missing value.

	.. versionadded:: 0.1.0
	"""
	holds_times = holds_only_times(OBJECT_TIMES)

	assert holds_times


def test_holds_only_times_refuses_other_arrays() -> None:
	"""
	Check numbers, mixed objects, times with a zone and missing values alone.

	.. versionadded:: 0.1.0
	"""
	refused_arrays = [INTEGERS, MIXED_OBJECTS, ZONED_TIMES, ONLY_MISSING]

	answers = [holds_only_times(values) for values in refused_arrays]

	assert not any(answers)


def test_store_time_objects_keeps_the_shape() -> None:
	"""
	Check that an object array becomes microseconds of the same shape.

	.. versionadded:: 0.1.0
	"""
	stored_times = store_time_objects(OBJECT_TIMES)

	assert stored_times.dtype == TIME_DTYPE
	assert stored_times.shape == OBJECT_TIMES.shape


def test_write_time_adds_microseconds_only_when_present() -> None:
	"""
	Check both texts of a time.

	.. versionadded:: 0.1.0
	"""
	short_text = write_time(SHORT_AFTERNOON)
	long_text = write_time(AFTERNOON)

	assert short_text == EXPECTED_SHORT_TEXT
	assert long_text == EXPECTED_LONG_TEXT

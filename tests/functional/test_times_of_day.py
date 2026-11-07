"""
Functional tests of the times of day of Arrays and Tables.

.. versionadded:: 0.1.0
"""

from datetime import UTC, time, timedelta

import numpy
import pandas
import pytest

import numdaplot as ndp

ACCIDENT_TIMES = [time(15, 35), time(8, 0), None, time(23, 59, 59, 999999)]
EXPECTED_ARRAY_TEXT = "Array(['15:35:00', '08:00:00', 'NaT', '23:59:59.999999'], dtype=TIME)"
EXPECTED_TABLE_TEXT = (
	"              hrmn\n              TIME\n0         15:35:00\n1         08:00:00\n2              NaT\n"
	"3  23:59:59.999999"
)
MORNING = time(8, 0)
NIGHT = time(22, 0)
EXPECTED_MORNING_FLAGS = [False, True, False, False]
EXPECTED_SORTED = [time(8, 0), time(15, 35), time(23, 59, 59, 999999), None]
MICROSECOND_WAITS = pandas.Series(numpy.array([5], dtype="timedelta64[us]"))
NUMPY_WAITS = numpy.array([5], dtype="timedelta64[us]")
ONE_HOUR = timedelta(hours=1)
ZONED_TIME = time(8, tzinfo=UTC)


def build_accident_times() -> ndp.Array:
	"""
	Return the hours of four accidents, one of them missing.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Array
		A TIME Array.
	"""
	times = ndp.Array.from_list(ACCIDENT_TIMES)

	return times


def test_an_array_of_times_shows_and_gives_back_its_times() -> None:
	"""
	Check the type, the text, to_list and to_numpy of an Array of times.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()

	array_text = repr(times)
	time_list = times.to_list()
	numpy_values = times.to_numpy()
	numpy_list = numpy_values.tolist()
	assert times.dtype == ndp.Type.TIME
	assert array_text == EXPECTED_ARRAY_TEXT
	assert time_list == ACCIDENT_TIMES
	assert numpy_list == ACCIDENT_TIMES


def test_a_table_of_times_goes_to_pandas_and_back() -> None:
	"""
	Check the display of a Table of times, and its round trip through pandas as datetime.time objects.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()
	accidents = ndp.Table.from_arrays({"hrmn": times})

	table_text = str(accidents)
	frame = accidents.to_pandas()
	read_accidents = ndp.Table.from_pandas(frame)

	frame_column = frame["hrmn"]
	frame_times = frame_column.tolist()
	is_same_table = read_accidents.is_equal(ndp.Equality(other=accidents))
	assert table_text == EXPECTED_TABLE_TEXT
	assert frame_times == ACCIDENT_TIMES
	assert is_same_table


def test_rules_compare_times_of_day() -> None:
	"""
	Check Equal on an Array and Greater in a Table filter.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()
	accidents = ndp.Table.from_arrays({"hrmn": times})

	morning_flags = times.check(ndp.Equal(MORNING))
	night = accidents.filter(ndp.Filter(conditions=[ndp.Condition(rule=ndp.Greater(NIGHT))]))

	morning_list = morning_flags.to_list()
	assert morning_list == EXPECTED_MORNING_FLAGS
	assert night.row_count == 1


def test_times_are_sorted_with_missing_values_last() -> None:
	"""
	Check the sort of an Array of times.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()

	sorted_times = times.sort()

	sorted_list = sorted_times.to_list()
	assert sorted_list == EXPECTED_SORTED


def test_outside_durations_in_microseconds_stay_durations() -> None:
	"""
	Check that pandas and numpy durations in microseconds give DURATION, never TIME.

	.. versionadded:: 0.1.0
	"""
	wait_frame = pandas.DataFrame({"wait": MICROSECOND_WAITS})
	waits = ndp.Table.from_pandas(wait_frame)

	numpy_waits = ndp.Array.from_numpy(NUMPY_WAITS)

	assert waits.column_types["wait"] == ndp.Type.DURATION
	assert numpy_waits.dtype == ndp.Type.DURATION


def test_a_mean_of_times_is_refused() -> None:
	"""
	Check that the mean of times of day raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()

	with pytest.raises(ndp.IncompatibleTypesError):
		times.compute(ndp.Mean())


def test_a_time_is_never_compared_with_a_duration() -> None:
	"""
	Check that a duration given to a rule on times raises IncompatibleTypesError.

	.. versionadded:: 0.1.0
	"""
	times = build_accident_times()

	with pytest.raises(ndp.IncompatibleTypesError):
		times.check(ndp.Equal(ONE_HOUR))


def test_a_time_with_a_time_zone_is_refused() -> None:
	"""
	Check that a time of day with a zone raises TimeZoneMismatchError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.TimeZoneMismatchError):
		ndp.Array.from_list([ZONED_TIME])

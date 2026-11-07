"""
Unit tests of the texts of datetimes and durations.

.. versionadded:: 0.1.0
"""

import numpy

from numdaplot.arrays.conversion.time_text import (
	find_datetime_unit,
	format_datetimes,
	format_durations,
	format_fractions,
	format_times,
	join_clock_parts,
	join_texts,
)

WHOLE_SECONDS = numpy.array(["2026-01-02T10:30:00", "NaT"], dtype="datetime64[ns]")
MIXED_FRACTIONS = numpy.array(["2026-01-02T10:30:00.25", "2026-01-02T11:00:00"], dtype="datetime64[ns]")
NANOSECONDS = numpy.array(["2026-01-02T10:30:00.000000001"], dtype="datetime64[ns]")
EMPTY_DATETIMES = numpy.array([], dtype="datetime64[ns]")
EXPECTED_WHOLE_TEXTS = ["2026-01-02 10:30:00", "NaT"]
EXPECTED_MIXED_TEXTS = ["2026-01-02 10:30:00.250", "2026-01-02 11:00:00.000"]
SECOND_UNIT = "s"
MILLISECOND_UNIT = "ms"
NANOSECOND_UNIT = "ns"
DURATIONS = numpy.array([86_400, 129_600, -43_200], dtype="timedelta64[s]")
GRID_DURATIONS = numpy.array([[3_600], [7_200]], dtype="timedelta64[s]")
FRACTION_DURATIONS = numpy.array([1_500, 0], dtype="timedelta64[ns]")
MISSING_DURATIONS = numpy.array(["NaT"], dtype="timedelta64[ns]")
EXPECTED_DURATION_TEXTS = ["1 days 00:00:00", "1 days 12:00:00", "-1 days +12:00:00"]
EXPECTED_GRID_TEXTS = [["0 days 01:00:00"], ["0 days 02:00:00"]]
EXPECTED_FRACTION_TEXTS = ["0 days 00:00:00.000001500", "0 days 00:00:00"]
EXPECTED_MISSING_TEXTS = ["NaT"]
CLOCK_PARTS = [numpy.array([9, 23]), numpy.array([5, 59]), numpy.array([0, 1])]
EXPECTED_CLOCK_TEXTS = ["09:05:00", "23:59:01"]
FRACTIONS = numpy.array([0, 250_000_000])
NUMBER_TEXTS = numpy.array(["1", "2"])
DAYS_SUFFIX = " days"
EXPECTED_JOINED_TEXTS = ["1 days", "2 days"]
EXPECTED_FRACTIONS = ["", ".250000000"]
TIME_GRID = numpy.array([[56100250000, "NaT"]], dtype="timedelta64[us]")
EXPECTED_TIME_TEXTS = [["15:35:00.250000", "NaT"]]


def test_format_datetimes_writes_whole_seconds_without_fraction() -> None:
	"""
	Check datetimes without fraction, a missing one written NaT.

	.. versionadded:: 0.1.0
	"""
	texts = format_datetimes(WHOLE_SECONDS)

	text_list = texts.tolist()
	assert text_list == EXPECTED_WHOLE_TEXTS


def test_format_datetimes_writes_every_value_with_the_same_fraction_digits() -> None:
	"""
	Check that a fraction on one value gives milliseconds to every value.

	.. versionadded:: 0.1.0
	"""
	texts = format_datetimes(MIXED_FRACTIONS)

	text_list = texts.tolist()
	assert text_list == EXPECTED_MIXED_TEXTS


def test_find_datetime_unit_chooses_the_shortest_exact_unit() -> None:
	"""
	Check seconds, milliseconds and nanoseconds.

	.. versionadded:: 0.1.0
	"""
	whole_unit = find_datetime_unit(WHOLE_SECONDS)
	mixed_unit = find_datetime_unit(MIXED_FRACTIONS)
	finest_unit = find_datetime_unit(NANOSECONDS)

	assert whole_unit == SECOND_UNIT
	assert mixed_unit == MILLISECOND_UNIT
	assert finest_unit == NANOSECOND_UNIT


def test_find_datetime_unit_uses_seconds_without_value() -> None:
	"""
	Check that no datetime gives seconds.

	.. versionadded:: 0.1.0
	"""
	unit = find_datetime_unit(EMPTY_DATETIMES)

	assert unit == SECOND_UNIT


def test_format_durations_writes_days_then_the_time() -> None:
	"""
	Check whole days, hours and a negative duration as pandas writes them.

	.. versionadded:: 0.1.0
	"""
	texts = format_durations(DURATIONS)

	text_list = texts.tolist()
	assert text_list == EXPECTED_DURATION_TEXTS


def test_format_durations_keeps_the_shape() -> None:
	"""
	Check a two-dimensional Array.

	.. versionadded:: 0.1.0
	"""
	texts = format_durations(GRID_DURATIONS)

	text_rows = texts.tolist()
	assert text_rows == EXPECTED_GRID_TEXTS


def test_format_durations_writes_fractions_only_where_they_exist() -> None:
	"""
	Check the nine digits of a fraction.

	.. versionadded:: 0.1.0
	"""
	texts = format_durations(FRACTION_DURATIONS)

	text_list = texts.tolist()
	assert text_list == EXPECTED_FRACTION_TEXTS


def test_format_durations_writes_nat_for_a_missing_value() -> None:
	"""
	Check a missing duration.

	.. versionadded:: 0.1.0
	"""
	texts = format_durations(MISSING_DURATIONS)

	text_list = texts.tolist()
	assert text_list == EXPECTED_MISSING_TEXTS


def test_join_clock_parts_writes_two_digits_each() -> None:
	"""
	Check hours, minutes and seconds joined by colons.

	.. versionadded:: 0.1.0
	"""
	texts = join_clock_parts(CLOCK_PARTS)

	text_list = texts.tolist()
	assert text_list == EXPECTED_CLOCK_TEXTS


def test_format_fractions_leaves_whole_seconds_empty() -> None:
	"""
	Check an empty text without fraction and nine digits with one.

	.. versionadded:: 0.1.0
	"""
	texts = format_fractions(FRACTIONS)

	text_list = texts.tolist()
	assert text_list == EXPECTED_FRACTIONS


def test_join_texts_adds_a_text_after_each_value() -> None:
	"""
	Check texts joined with a single text.

	.. versionadded:: 0.1.0
	"""
	joined_texts = join_texts(NUMBER_TEXTS, DAYS_SUFFIX)

	text_list = joined_texts.tolist()
	assert text_list == EXPECTED_JOINED_TEXTS


def test_format_times_keeps_the_shape_and_writes_nat() -> None:
	"""
	Check the texts of a grid of times.

	.. versionadded:: 0.1.0
	"""
	time_texts = format_times(TIME_GRID)

	text_list = time_texts.tolist()
	assert text_list == EXPECTED_TIME_TEXTS

"""
Unit tests of the comparison of values with a reference out of range.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime, timedelta

import numpy

from numdaplot.arrays.selection.time_reference import (
	compare_with_reference,
	find_far_side,
	is_far_reference,
	remove_far_references,
)

MOMENTS = numpy.array(["2026-01-31"], dtype="datetime64[ns]")
SECOND_MOMENTS = numpy.array(["2026-01-31"], dtype="datetime64[s]")
DAYS = numpy.array(["2026-01-31"], dtype="datetime64[D]")
NUMBERS = numpy.array([1.5])
FAR_MOMENT = datetime(3000, 1, 1)
OLD_MOMENT = datetime(1000, 1, 1)
NEAR_MOMENT = datetime(2026, 1, 31)
FAR_DURATION = timedelta(days=200000)


def test_is_far_reference_finds_a_moment_out_of_range() -> None:
	"""
	Check a datetime beside nanoseconds.

	.. versionadded:: 0.1.0
	"""
	is_far = is_far_reference(MOMENTS, FAR_MOMENT)

	assert is_far is True


def test_is_far_reference_leaves_a_moment_in_range() -> None:
	"""
	Check a usual datetime.

	.. versionadded:: 0.1.0
	"""
	is_far = is_far_reference(MOMENTS, NEAR_MOMENT)

	assert is_far is False


def test_is_far_reference_leaves_values_in_a_coarser_unit() -> None:
	"""
	Check values numpy compares itself, as they hold the same range.

	.. versionadded:: 0.1.0
	"""
	far_for_seconds = is_far_reference(SECOND_MOMENTS, FAR_MOMENT)
	far_for_days = is_far_reference(DAYS, FAR_MOMENT)

	assert far_for_seconds is False
	assert far_for_days is False


def test_is_far_reference_leaves_other_values() -> None:
	"""
	Check numbers.

	.. versionadded:: 0.1.0
	"""
	is_far = is_far_reference(NUMBERS, 1.5)

	assert is_far is False


def test_find_far_side_reads_each_kind_of_reference() -> None:
	"""
	Check dates, datetimes and durations on both sides.

	.. versionadded:: 0.1.0
	"""
	sides = [
		find_far_side(FAR_MOMENT),
		find_far_side(OLD_MOMENT),
		find_far_side(date(3000, 1, 1)),
		find_far_side(FAR_DURATION),
		find_far_side(-FAR_DURATION),
	]

	assert sides == [1, -1, 1, 1, -1]


def test_compare_with_reference_answers_for_every_value() -> None:
	"""
	Check the shape of the answer.

	.. versionadded:: 0.1.0
	"""
	moments = numpy.array([["2026-01-31", "2020-01-01"]], dtype="datetime64[ns]")

	matches = compare_with_reference(moments, FAR_MOMENT, numpy.less)

	match_list = matches.tolist()
	assert match_list == [[True, True]]


def test_compare_with_reference_compares_a_near_reference() -> None:
	"""
	Check a reference numpy can convert.

	.. versionadded:: 0.1.0
	"""
	matches = compare_with_reference(MOMENTS, NEAR_MOMENT, numpy.equal)

	match_list = matches.tolist()
	assert match_list == [True]


def test_remove_far_references_keeps_the_order_of_the_others() -> None:
	"""
	Check a list mixing both kinds.

	.. versionadded:: 0.1.0
	"""
	references = [FAR_MOMENT, NEAR_MOMENT, OLD_MOMENT]

	near_references = remove_far_references(MOMENTS, references)

	assert near_references == [NEAR_MOMENT]


def test_is_far_reference_finds_a_duration_too_long_for_microseconds() -> None:
	"""
	Check durations stored in microseconds.

	.. versionadded:: 0.1.0
	"""
	durations = numpy.array([5], dtype="timedelta64[us]")

	is_far = is_far_reference(durations, timedelta.max)

	assert is_far is True


def test_is_far_reference_leaves_a_duration_microseconds_can_count() -> None:
	"""
	Check a duration beyond nanoseconds but within microseconds.

	.. versionadded:: 0.1.0
	"""
	durations = numpy.array([5], dtype="timedelta64[us]")

	is_far = is_far_reference(durations, FAR_DURATION)

	assert is_far is False


def test_is_far_reference_leaves_a_duration_of_a_coarser_unit() -> None:
	"""
	Check durations in seconds, which can hold the longest Python duration.

	.. versionadded:: 0.1.0
	"""
	durations = numpy.array([5], dtype="timedelta64[s]")

	is_far = is_far_reference(durations, timedelta.max)

	assert is_far is False

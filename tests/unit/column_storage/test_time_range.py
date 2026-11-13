"""
Unit tests of the range of times a count of nanoseconds holds.

.. versionadded:: 0.2.0
"""

from datetime import UTC, date, datetime, timedelta

import pytest

from numdaplot.column_storage.time_range import (
	HIGHEST_DATETIME,
	LONGEST_DURATION,
	LOWEST_DATETIME,
	is_python_time_in_range,
)

ONE_MICROSECOND = timedelta(microseconds=1)
FAR_DATETIME = datetime(3000, 1, 1)
FAR_DATE = date(3000, 1, 1)
CLOSE_DATE = date(2026, 1, 31)


@pytest.mark.parametrize(
	"value",
	[HIGHEST_DATETIME, LOWEST_DATETIME, LONGEST_DURATION, -LONGEST_DURATION, CLOSE_DATE, 5, "text", None],
)
def test_is_python_time_in_range_accepts_the_limits_and_other_values(value: object) -> None:
	"""
	Check the limits of the range, and that other values are not concerned.

	.. versionadded:: 0.1.0
	"""
	in_range = is_python_time_in_range(value)

	assert in_range is True


@pytest.mark.parametrize(
	"value",
	[
		HIGHEST_DATETIME + ONE_MICROSECOND,
		LOWEST_DATETIME - ONE_MICROSECOND,
		LONGEST_DURATION + ONE_MICROSECOND,
		-LONGEST_DURATION - ONE_MICROSECOND,
		FAR_DATE,
	],
)
def test_is_python_time_in_range_refuses_what_follows_the_limits(value: object) -> None:
	"""
	Check the first values out of range.

	.. versionadded:: 0.1.0
	"""
	in_range = is_python_time_in_range(value)

	assert in_range is False


def test_is_python_time_in_range_reads_a_datetime_with_a_zone_by_its_clock_time() -> None:
	"""
	Check that a time zone does not stop the comparison.

	.. versionadded:: 0.1.0
	"""
	far_with_zone = FAR_DATETIME.replace(tzinfo=UTC)

	in_range = is_python_time_in_range(far_with_zone)

	assert in_range is False

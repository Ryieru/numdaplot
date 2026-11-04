"""
Unit tests of the change of the time zone of a datetime column.

.. versionadded:: 0.1.0
"""

import pandas
import pytest

from numdaplot.dates.time_zone import TimeZone
from numdaplot.dates.time_zone_change import TimeZoneChange
from numdaplot.dates.time_zone_mode import TimeZoneMode
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.errors.value_conversion_error import ValueConversionError
from numdaplot.tables.columns.time_zone_conversion import attribute_time_zone, change_time_zone
from numdaplot.tables.frames.time_zones import find_column_time_zone

PARIS_NAME = "Europe/Paris"
PARIS = TimeZone(PARIS_NAME)
NEW_YORK = TimeZone("America/New_York")
ATTRIBUTE_PARIS = TimeZoneChange(mode=TimeZoneMode.ATTRIBUTE, zone=PARIS)
SHIFT_NEW_YORK = TimeZoneChange(mode=TimeZoneMode.SHIFT, zone=NEW_YORK)
REMOVE_ZONE = TimeZoneChange(mode=TimeZoneMode.REMOVE)
NAIVE_TIMES = pandas.Series(pandas.to_datetime(["2026-07-01 10:30", "NaT"])).astype("datetime64[ns]")
PARIS_TIMES = NAIVE_TIMES.dt.tz_localize(PARIS_NAME)
SPRING_GAP = pandas.Series(pandas.to_datetime(["2026-07-01 10:30", "2026-03-29 02:30"])).astype("datetime64[ns]")
AUTUMN_TWICE = pandas.Series(pandas.to_datetime(["2026-10-25 02:30"])).astype("datetime64[ns]")
EXPECTED_PARIS_TIME = pandas.Timestamp("2026-07-01 10:30", tz=PARIS_NAME)
EXPECTED_NEW_YORK_TIME = pandas.Timestamp("2026-07-01 04:30", tz="America/New_York")
EXPECTED_CLOCK_TIME = pandas.Timestamp("2026-07-01 10:30")
EXPECTED_GAP_TEXT = "2026-03-29 02:30:00"


def test_change_time_zone_attributes_a_zone_keeping_the_clock_time() -> None:
	"""
	Check that 10:30 without zone becomes 10:30 in Paris, a missing value staying missing.

	.. versionadded:: 0.1.0
	"""
	paris_times = change_time_zone(NAIVE_TIMES, ATTRIBUTE_PARIS)

	time_zone = find_column_time_zone(paris_times)
	missing = paris_times.isna()
	is_second_missing = bool(missing.iloc[1])
	assert time_zone == PARIS
	assert paris_times.iloc[0] == EXPECTED_PARIS_TIME
	assert is_second_missing


def test_change_time_zone_shifts_keeping_the_instant() -> None:
	"""
	Check that 10:30 in Paris is 04:30 in New York.

	.. versionadded:: 0.1.0
	"""
	new_york_times = change_time_zone(PARIS_TIMES, SHIFT_NEW_YORK)

	assert new_york_times.iloc[0] == EXPECTED_NEW_YORK_TIME


def test_change_time_zone_removes_the_zone_keeping_the_clock_time() -> None:
	"""
	Check that 10:30 in Paris becomes 10:30 without zone.

	.. versionadded:: 0.1.0
	"""
	naive_times = change_time_zone(PARIS_TIMES, REMOVE_ZONE)

	time_zone = find_column_time_zone(naive_times)
	assert time_zone is None
	assert naive_times.iloc[0] == EXPECTED_CLOCK_TIME


@pytest.mark.parametrize(
	("times", "change"),
	[(PARIS_TIMES, ATTRIBUTE_PARIS), (NAIVE_TIMES, SHIFT_NEW_YORK), (NAIVE_TIMES, REMOVE_ZONE)],
)
def test_change_time_zone_rejects_a_change_that_does_not_fit_the_zone_state(
	times: pandas.Series,
	change: TimeZoneChange,
) -> None:
	"""
	Check that attributing to a zone column, or shifting and removing without zone, raise TimeZoneMismatchError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	times
		A datetime column.
	change
		A change that does not fit it.
	"""
	with pytest.raises(TimeZoneMismatchError):
		change_time_zone(times, change)


def test_attribute_time_zone_cites_a_clock_time_that_does_not_exist() -> None:
	"""
	Check that 02:30 on the spring change in Paris raises ValueConversionError citing it.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError) as caught:
		attribute_time_zone(SPRING_GAP, PARIS_NAME)

	assert caught.value.rejected_value == EXPECTED_GAP_TEXT


def test_attribute_time_zone_rejects_a_clock_time_that_exists_twice() -> None:
	"""
	Check that 02:30 on the autumn change in Paris raises ValueConversionError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ValueConversionError):
		attribute_time_zone(AUTUMN_TWICE, PARIS_NAME)

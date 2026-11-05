"""
Unit tests of CustomDateFormat, TimeZone, TimeZoneChange and the time functions.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.dates.custom_date_format import CustomDateFormat
from numdaplot.dates.date_part import DatePart
from numdaplot.dates.date_part_unit import DatePartUnit
from numdaplot.dates.date_period import DatePeriod
from numdaplot.dates.duration_in import DurationIn
from numdaplot.dates.duration_unit import DurationUnit
from numdaplot.dates.period_unit import PeriodUnit
from numdaplot.dates.time_function import TimeFunction
from numdaplot.dates.time_zone import TimeZone
from numdaplot.dates.time_zone_change import TimeZoneChange
from numdaplot.dates.time_zone_mode import TimeZoneMode
from numdaplot.dates.to_duration import ToDuration
from numdaplot.errors.invalid_date_format_error import InvalidDateFormatError
from numdaplot.errors.invalid_time_zone_change_error import InvalidTimeZoneChangeError
from numdaplot.errors.unknown_time_zone_error import UnknownTimeZoneError

DATE_PATTERN = "%d %b %Y"
REJECTED_PATTERNS = ["%H:%M", "%Y-%m-%d %z", "day"]
ZONE_NAMES = ["Europe/Paris", "UTC", "America/New_York"]
REJECTED_ZONE_NAMES = ["Paris", "+01:00", ""]
PARIS = TimeZone("Europe/Paris")
TIME_FUNCTIONS = [
	DatePart(unit=DatePartUnit.MONTH),
	DatePeriod(unit=PeriodUnit.WEEK),
	DurationIn(unit=DurationUnit.DAY),
	ToDuration(unit=DurationUnit.HOUR),
]


def test_custom_date_format_keeps_a_date_pattern() -> None:
	"""
	Check that a pattern with date codes is accepted as given.

	.. versionadded:: 0.1.0
	"""
	date_format = CustomDateFormat(DATE_PATTERN)

	assert date_format.pattern == DATE_PATTERN


@pytest.mark.parametrize("pattern", REJECTED_PATTERNS)
def test_custom_date_format_rejects_a_pattern_without_date_or_with_a_zone(pattern: str) -> None:
	"""
	Check that a pattern without day, month or year code, or with a time zone code, raises InvalidDateFormatError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	pattern
		A rejected pattern.
	"""
	with pytest.raises(InvalidDateFormatError):
		CustomDateFormat(pattern)


@pytest.mark.parametrize("zone_name", ZONE_NAMES)
def test_time_zone_accepts_an_iana_name(zone_name: str) -> None:
	"""
	Check that IANA names are accepted.

	.. versionadded:: 0.1.0

	Parameters
	----------
	zone_name
		An IANA name.
	"""
	time_zone = TimeZone(zone_name)

	assert time_zone.name == zone_name


@pytest.mark.parametrize("zone_name", REJECTED_ZONE_NAMES)
def test_time_zone_rejects_a_name_that_is_not_an_iana_name(zone_name: str) -> None:
	"""
	Check that a city alone, a fixed offset and an empty name raise UnknownTimeZoneError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	zone_name
		A rejected name.
	"""
	with pytest.raises(UnknownTimeZoneError):
		TimeZone(zone_name)


@pytest.mark.parametrize("mode", [TimeZoneMode.ATTRIBUTE, TimeZoneMode.SHIFT])
def test_time_zone_change_needs_a_zone_to_attribute_or_shift(mode: TimeZoneMode) -> None:
	"""
	Check that ATTRIBUTE and SHIFT without zone raise InvalidTimeZoneChangeError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	mode
		A mode needing a zone.
	"""
	with pytest.raises(InvalidTimeZoneChangeError):
		TimeZoneChange(mode=mode)


def test_time_zone_change_refuses_a_zone_to_remove() -> None:
	"""
	Check that REMOVE with a zone raises InvalidTimeZoneChangeError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidTimeZoneChangeError):
		TimeZoneChange(mode=TimeZoneMode.REMOVE, zone=PARIS)


def test_time_zone_change_keeps_its_mode_and_zone() -> None:
	"""
	Check an accepted change.

	.. versionadded:: 0.1.0
	"""
	change = TimeZoneChange(mode=TimeZoneMode.SHIFT, zone=PARIS)

	assert change.mode == TimeZoneMode.SHIFT
	assert change.zone == PARIS


@pytest.mark.parametrize("function", TIME_FUNCTIONS)
def test_every_time_function_is_a_time_function(function: TimeFunction) -> None:
	"""
	Check that DatePart, DatePeriod, DurationIn and ToDuration share the TimeFunction base.

	.. versionadded:: 0.1.0

	Parameters
	----------
	function
		A time function.
	"""
	assert isinstance(function, TimeFunction)

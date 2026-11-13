"""
Unit tests of the matching of the datetimes of a rule with the time zone of a column.

.. versionadded:: 0.1.0
"""

from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

import pytest

from numdaplot.dates.time_zone import TimeZone
from numdaplot.errors.dates.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.rules.between import Between
from numdaplot.rules.greater import Greater
from numdaplot.rules.is_in import IsIn
from numdaplot.rules.is_missing import IsMissing
from numdaplot.tables.filtering.rule_moments import (
	match_field_time_zone,
	match_moment_time_zone,
	match_rule_time_zone,
)

PARIS = TimeZone("Europe/Paris")
PARIS_INFO = ZoneInfo("Europe/Paris")
PARIS_NOON = datetime(2026, 7, 1, 12, tzinfo=PARIS_INFO)
UTC_TEN = datetime(2026, 7, 1, 10)
UTC_MORNING = datetime(2026, 7, 1, 8, tzinfo=UTC)
NAIVE_NOON = datetime(2026, 7, 1, 12)
NEW_YEAR = date(2026, 1, 1)
NUMBER_LIMIT = 10
NUMBERS = [1, 2]
EXPECTED_UTC_MORNING = datetime(2026, 7, 1, 8)


def test_match_rule_time_zone_moves_the_datetimes_to_utc_for_a_zone_column() -> None:
	"""
	Check that noon in Paris in summer becomes 10:00 without zone.

	.. versionadded:: 0.1.0
	"""
	matched_rule = match_rule_time_zone(Greater(PARIS_NOON), PARIS)

	assert matched_rule == Greater(UTC_TEN)


def test_match_rule_time_zone_moves_every_bound_and_listed_value() -> None:
	"""
	Check Between and IsIn.

	.. versionadded:: 0.1.0
	"""
	matched_between = match_rule_time_zone(Between(UTC_MORNING, PARIS_NOON), PARIS)
	matched_is_in = match_rule_time_zone(IsIn([UTC_MORNING]), PARIS)

	assert matched_between == Between(EXPECTED_UTC_MORNING, UTC_TEN)
	assert matched_is_in == IsIn([EXPECTED_UTC_MORNING])


def test_match_rule_time_zone_keeps_the_rule_of_a_column_without_zone() -> None:
	"""
	Check that a rule without datetime with a zone is returned as it is.

	.. versionadded:: 0.1.0
	"""
	rule = Greater(NAIVE_NOON)

	matched_rule = match_rule_time_zone(rule, None)

	assert matched_rule is rule


def test_match_rule_time_zone_keeps_a_rule_without_settings() -> None:
	"""
	Check IsMissing on a zone column.

	.. versionadded:: 0.1.0
	"""
	rule = IsMissing()

	matched_rule = match_rule_time_zone(rule, PARIS)

	assert matched_rule == rule


@pytest.mark.parametrize("value", [NAIVE_NOON, NEW_YEAR])
def test_match_moment_time_zone_rejects_a_value_without_zone_for_a_zone_column(value: date) -> None:
	"""
	Check that a date or a datetime without zone raises TimeZoneMismatchError on a zone column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		A date or a datetime without zone.
	"""
	with pytest.raises(TimeZoneMismatchError):
		match_moment_time_zone(value, PARIS)


def test_match_moment_time_zone_rejects_a_zone_value_for_a_column_without_zone() -> None:
	"""
	Check that a datetime with a zone raises TimeZoneMismatchError on a column without zone.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(TimeZoneMismatchError):
		match_moment_time_zone(PARIS_NOON, None)


def test_match_moment_time_zone_keeps_other_values() -> None:
	"""
	Check that a number stays the same, whatever the zone.

	.. versionadded:: 0.1.0
	"""
	matched_value = match_moment_time_zone(NUMBER_LIMIT, PARIS)

	assert matched_value == NUMBER_LIMIT


def test_match_field_time_zone_matches_each_value_of_a_list() -> None:
	"""
	Check a list of numbers.

	.. versionadded:: 0.1.0
	"""
	matched_values = match_field_time_zone(NUMBERS, PARIS)

	assert matched_values == NUMBERS

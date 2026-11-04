"""
Datetimes of a rule matched with the time zone of the column it is applied to.

.. versionadded:: 0.1.0
"""

import dataclasses
from datetime import UTC, date, datetime
from typing import Any, cast

from numdaplot.dates.time_zone import TimeZone
from numdaplot.errors.time_zone_mismatch_error import TimeZoneMismatchError
from numdaplot.rules.rule import Rule

NAIVE_COLUMN_OPERATION = "A rule on a column without time zone"
ZONE_COLUMN_OPERATION = "A rule on a datetime column with a time zone"


def match_rule_time_zone(rule: Rule, time_zone: TimeZone | None) -> Rule:
	"""
	Return a rule whose dates and datetimes can be compared with the values of a column.

	A column with a time zone is compared through its UTC clock times, so the datetimes of the rule are
	moved to UTC too.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rule
		Any rule of numdaplot.
	time_zone
		The time zone of the column, ``None`` when it has none.

	Returns
	-------
	Rule
		The rule itself for a column without time zone, or a copy with its datetimes as UTC clock times
		without zone.

	Raises
	------
	TimeZoneMismatchError
		When the rule has a datetime with a time zone and the column has none, or the column has a zone and
		the rule has a date or a datetime without zone.

	Examples
	--------
	>>> from datetime import datetime
	>>> from zoneinfo import ZoneInfo
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.filtering.rule_moments import match_rule_time_zone
	>>> paris_noon = datetime(2026, 7, 1, 12, tzinfo=ZoneInfo("Europe/Paris"))
	>>> match_rule_time_zone(ndp.Greater(paris_noon), ndp.TimeZone("Europe/Paris"))
	Greater(value=datetime.datetime(2026, 7, 1, 10, 0))
	"""
	if not dataclasses.is_dataclass(rule):
		return rule

	rule_fields = dataclasses.fields(rule)
	matched_values = dict[str, Any]()

	for rule_field in rule_fields:
		field_value = getattr(rule, rule_field.name)
		matched_values[rule_field.name] = match_field_time_zone(field_value, time_zone)

	if time_zone is None:
		return rule

	matched_rule = dataclasses.replace(rule, **matched_values)

	return matched_rule


def match_field_time_zone(field_value: Any, time_zone: TimeZone | None) -> Any:
	"""
	Return the value of a rule setting with its dates and datetimes matched with the zone of a column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	field_value
		The value of a setting of a rule, a single value or a list of values.
	time_zone
		The time zone of the column, ``None`` when it has none.

	Returns
	-------
	Any
		The value, a datetime moved to a UTC clock time without zone, or a list of such values.

	Raises
	------
	TimeZoneMismatchError
		When a date or a datetime does not match the zone state of the column.

	Examples
	--------
	>>> from numdaplot.tables.filtering.rule_moments import match_field_time_zone
	>>> match_field_time_zone([1, 2], None)
	[1, 2]
	"""
	if isinstance(field_value, list):
		list_values = cast(list[Any], field_value)
		matched_list = [match_moment_time_zone(list_value, time_zone) for list_value in list_values]
		return matched_list

	matched_value = match_moment_time_zone(field_value, time_zone)

	return matched_value


def match_moment_time_zone(value: Any, time_zone: TimeZone | None) -> Any:
	"""
	Return a single value of a rule with its date or datetime matched with the zone of a column.

	.. versionadded:: 0.1.0

	Parameters
	----------
	value
		A single value of a rule.
	time_zone
		The time zone of the column, ``None`` when it has none.

	Returns
	-------
	Any
		The value itself, or a datetime with a zone moved to a UTC clock time without zone.

	Raises
	------
	TimeZoneMismatchError
		When the value is a datetime with a zone and the column has none, or the column has a zone and the value
		is a date or a datetime without zone.

	Examples
	--------
	>>> from datetime import datetime
	>>> from zoneinfo import ZoneInfo
	>>> import numdaplot as ndp
	>>> from numdaplot.tables.filtering.rule_moments import match_moment_time_zone
	>>> match_moment_time_zone(datetime(2026, 1, 1, 9, tzinfo=ZoneInfo("Europe/Paris")), ndp.TimeZone("UTC"))
	datetime.datetime(2026, 1, 1, 8, 0)
	"""
	if not isinstance(value, date):
		return value

	has_zone = isinstance(value, datetime) and value.tzinfo is not None
	if time_zone is None and has_zone:
		raise TimeZoneMismatchError(NAIVE_COLUMN_OPERATION, False)

	if time_zone is None:
		return value

	if not has_zone:
		raise TimeZoneMismatchError(ZONE_COLUMN_OPERATION, True)

	zone_datetime = cast(datetime, value)
	utc_datetime = zone_datetime.astimezone(UTC)
	naive_datetime = utc_datetime.replace(tzinfo=None)

	return naive_datetime

"""
Functional tests of the rules whose reference is a date, a datetime or a duration out of range.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta

import numpy
import pytest

import numdaplot as ndp

STORED_MOMENT = datetime(2000, 1, 1)
STORED_DATE = date(2000, 1, 1)
STORED_DURATION = timedelta(days=1)
FAR_MOMENT = datetime(3000, 1, 1)
OLD_MOMENT = datetime(1000, 1, 1)
FAR_DATE = date(3000, 1, 1)
FAR_DURATION = timedelta(days=200000)
NEGATIVE_DURATION = timedelta(days=-200000)
SENTINEL_MOMENT = datetime(9999, 12, 31)
COLUMN_NAME = "when"


@dataclass(frozen=True)
class RuleCase:
	"""
	A rule, and whether a stored value satisfies it.

	.. versionadded:: 0.1.0
	"""

	rule: ndp.Rule
	expected: bool


AFTER_EVERY_VALUE = [
	RuleCase(ndp.Greater(value=FAR_MOMENT), False),
	RuleCase(ndp.GreaterOrEqual(value=FAR_MOMENT), False),
	RuleCase(ndp.Less(value=FAR_MOMENT), True),
	RuleCase(ndp.LessOrEqual(value=FAR_MOMENT), True),
	RuleCase(ndp.Equal(value=FAR_MOMENT), False),
	RuleCase(ndp.NotEqual(value=FAR_MOMENT), True),
	RuleCase(ndp.IsIn(values=[FAR_MOMENT]), False),
	RuleCase(ndp.IsIn(values=[FAR_MOMENT, STORED_MOMENT]), True),
	RuleCase(ndp.Between(low=OLD_MOMENT, high=FAR_MOMENT), True),
	RuleCase(ndp.Between(low=FAR_MOMENT, high=SENTINEL_MOMENT), False),
	RuleCase(ndp.Less(value=SENTINEL_MOMENT), True),
	RuleCase(ndp.Less(value=FAR_DATE), True),
]
BEFORE_EVERY_VALUE = [
	RuleCase(ndp.Greater(value=OLD_MOMENT), True),
	RuleCase(ndp.Less(value=OLD_MOMENT), False),
]
DURATION_CASES = [
	RuleCase(ndp.Greater(value=FAR_DURATION), False),
	RuleCase(ndp.Less(value=FAR_DURATION), True),
	RuleCase(ndp.Greater(value=NEGATIVE_DURATION), True),
	RuleCase(ndp.Less(value=NEGATIVE_DURATION), False),
	RuleCase(ndp.Equal(value=FAR_DURATION), False),
]


@pytest.mark.parametrize("case", [*AFTER_EVERY_VALUE, *BEFORE_EVERY_VALUE])
def test_check_gives_the_right_answer_for_a_far_datetime(case: RuleCase) -> None:
	"""
	Check every comparison of a datetime in range with a reference out of range.

	.. versionadded:: 0.1.0
	"""
	moments = ndp.Array.from_list([STORED_MOMENT])

	mask = moments.check(case.rule)

	mask_list = mask.to_list()
	assert mask_list == [case.expected]


@pytest.mark.parametrize("case", DURATION_CASES)
def test_check_gives_the_right_answer_for_a_far_duration(case: RuleCase) -> None:
	"""
	Check the comparisons of a duration on both sides of zero.

	.. versionadded:: 0.1.0
	"""
	durations = ndp.Array.from_list([STORED_DURATION])

	mask = durations.check(case.rule)

	mask_list = mask.to_list()
	assert mask_list == [case.expected]


@pytest.mark.parametrize("rule", [ndp.Less(value=FAR_MOMENT), ndp.NotEqual(value=FAR_MOMENT)])
def test_a_missing_value_still_satisfies_no_rule(rule: ndp.Rule) -> None:
	"""
	Check that a far reference does not accept a missing value.

	.. versionadded:: 0.1.0
	"""
	moments = ndp.Array.from_list([None, STORED_MOMENT])

	mask = moments.check(rule)

	mask_list = mask.to_list()
	assert mask_list == [False, True]


def test_select_keeps_the_values_before_a_far_datetime() -> None:
	"""
	Check ``Array.select``.

	.. versionadded:: 0.1.0
	"""
	moments = ndp.Array.from_list([STORED_MOMENT])

	selected = moments.select(ndp.Less(value=SENTINEL_MOMENT))

	selected_list = selected.to_list()
	assert selected_list == [STORED_MOMENT]


def build_moment_table() -> ndp.Table:
	"""
	Return a Table with a column of datetimes.

	.. versionadded:: 0.1.0

	Returns
	-------
	ndp.Table
		The column ``when``.
	"""
	moments = ndp.Array.from_list([STORED_MOMENT])
	table = ndp.Table.from_arrays({COLUMN_NAME: moments})

	return table


@pytest.mark.parametrize(
	("rule", "expected_list"),
	[(ndp.Less(value=FAR_MOMENT), [STORED_MOMENT]), (ndp.Greater(value=FAR_MOMENT), [])],
)
def test_filter_gives_the_right_rows_for_a_far_datetime(rule: ndp.Rule, expected_list: list[datetime]) -> None:
	"""
	Check ``Table.filter`` on both sides.

	.. versionadded:: 0.1.0
	"""
	table = build_moment_table()
	condition = ndp.Condition(rule=rule, columns=[COLUMN_NAME])

	filtered_table = table.filter(ndp.Filter(conditions=[condition]))

	kept_moments = filtered_table.column(COLUMN_NAME)
	kept_list = kept_moments.to_list()
	assert kept_list == expected_list


def test_a_reference_in_range_compares_as_before() -> None:
	"""
	Check values on both sides of a usual reference.

	.. versionadded:: 0.1.0
	"""
	moments = ndp.Array.from_list([datetime(1999, 1, 1), datetime(2001, 1, 1)])

	mask = moments.check(ndp.Greater(value=STORED_MOMENT))

	mask_list = mask.to_list()
	assert mask_list == [False, True]


def test_dates_stored_in_days_compare_with_a_far_date() -> None:
	"""
	Check the type holding far values: a far value of the Array is not lost.

	.. versionadded:: 0.1.0
	"""
	dates = ndp.Array.from_list([STORED_DATE, FAR_DATE])

	mask = dates.check(ndp.Equal(value=FAR_DATE))

	mask_list = mask.to_list()
	assert mask_list == [False, True]


@pytest.mark.parametrize("dtype", ["timedelta64[us]", "timedelta64[ms]", "timedelta64[s]", "timedelta64[D]"])
@pytest.mark.parametrize(
	"case",
	[
		RuleCase(ndp.Greater(value=timedelta.max), False),
		RuleCase(ndp.Less(value=timedelta.max), True),
		RuleCase(ndp.Greater(value=timedelta.min), True),
		RuleCase(ndp.Less(value=timedelta.min), False),
		RuleCase(ndp.Equal(value=timedelta.max), False),
		RuleCase(ndp.IsIn(values=[timedelta.max]), False),
		RuleCase(ndp.Less(value=timedelta(days=109500000)), True),
	],
)
def test_a_very_long_duration_compares_with_durations_of_any_unit(dtype: str, case: RuleCase) -> None:
	"""
	Check durations beyond what microseconds can count, against durations of numpy in other units.

	.. versionadded:: 0.1.0
	"""
	values = numpy.array([5], dtype=dtype)
	durations = ndp.Array.from_numpy(values)

	mask = durations.check(case.rule)

	mask_list = mask.to_list()
	assert mask_list == [case.expected]


def test_a_very_long_duration_compares_with_an_equally_long_duration() -> None:
	"""
	Check that durations in seconds beyond microseconds are not treated as shorter than the reference.

	.. versionadded:: 0.1.0
	"""
	long_days = 200000000
	values = numpy.array([long_days], dtype="timedelta64[D]")
	durations = ndp.Array.from_numpy(values)

	mask = durations.check(ndp.Equal(value=timedelta(days=long_days)))

	mask_list = mask.to_list()
	assert mask_list == [True]

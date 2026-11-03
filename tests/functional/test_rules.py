"""
Functional tests of the rules, as a user creates them from ndp.

.. versionadded:: 0.1.0
"""

from datetime import date

import pytest

import numdaplot as ndp

THRESHOLD = 100
COUNTRY = "FR"
COUNTRIES = ["FR", "DE"]
SEARCHED_TEXT = "paris"
YEAR_START = date(2026, 1, 1)
YEAR_END = date(2026, 12, 31)
ALL_RULES = [
	ndp.Equal(COUNTRY),
	ndp.NotEqual(COUNTRY),
	ndp.Greater(THRESHOLD),
	ndp.GreaterOrEqual(THRESHOLD),
	ndp.Less(THRESHOLD),
	ndp.LessOrEqual(THRESHOLD),
	ndp.Between(low=YEAR_START, high=YEAR_END),
	ndp.IsIn(COUNTRIES),
	ndp.Contains(SEARCHED_TEXT, case=ndp.Case.IGNORED),
	ndp.IsMissing(),
	ndp.IsPresent(),
]


@pytest.mark.parametrize("rule", ALL_RULES)
def test_every_rule_is_a_rule(rule: ndp.Rule) -> None:
	"""
	Check that every rule exposed by ndp can be created and is a Rule.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rule
		A rule created from ndp.
	"""
	assert isinstance(rule, ndp.Rule)


def test_a_period_between_two_dates_keeps_its_bounds() -> None:
	"""
	Check that a user can describe a period with Between and choose its bounds.

	.. versionadded:: 0.1.0
	"""
	period = ndp.Between(low=YEAR_START, high=YEAR_END, bounds=ndp.Bounds.LOW_ONLY)

	assert period.low == YEAR_START
	assert period.high == YEAR_END
	assert period.bounds == ndp.Bounds.LOW_ONLY


def test_a_reversed_period_is_rejected() -> None:
	"""
	Check that a user describing a period backwards gets InvalidBoundsError.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(ndp.InvalidBoundsError):
		ndp.Between(low=YEAR_END, high=YEAR_START)

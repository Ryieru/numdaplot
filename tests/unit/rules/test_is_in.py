"""
Unit tests of IsIn.

.. versionadded:: 0.1.0
"""

import pytest

from numdaplot.errors.empty_values_error import EmptyValuesError
from numdaplot.rules.is_in import IsIn

ACCEPTED_COUNTRIES = ["FR", "DE"]
ADDED_COUNTRY = "IT"


def test_is_in_keeps_the_accepted_values() -> None:
	"""
	Check that the accepted values are available as an attribute.

	.. versionadded:: 0.1.0
	"""
	rule = IsIn(ACCEPTED_COUNTRIES)

	assert rule.values == ACCEPTED_COUNTRIES


def test_is_in_is_not_changed_by_a_later_change_of_the_given_list() -> None:
	"""
	Check that the rule holds its own copy of the list.

	.. versionadded:: 0.1.0
	"""
	given_values = list(ACCEPTED_COUNTRIES)
	rule = IsIn(given_values)

	given_values.append(ADDED_COUNTRY)

	assert rule.values == ACCEPTED_COUNTRIES


def test_is_in_rejects_an_empty_list() -> None:
	"""
	Check that an empty list of accepted values is rejected.

	.. versionadded:: 0.1.0
	"""
	empty_values = list[str]()

	with pytest.raises(EmptyValuesError):
		IsIn(empty_values)

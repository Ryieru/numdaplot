"""
Unit tests of IsIn.

.. versionadded:: 0.1.0
"""

from typing import Any, TypeVar, cast

import pytest

from numdaplot.errors.empty_values_error import EmptyValuesError
from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.rules.is_in import IsIn
from numdaplot.rules.rule_values import ScalarValue

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


def test_is_in_type_parameter_holds_the_types_of_its_alias() -> None:
	"""
	Check that the type parameter shown as ScalarValue accepts exactly the types of this alias.

	.. versionadded:: 0.1.0
	"""
	type_parameter = IsIn.__type_params__[0]
	assert isinstance(type_parameter, TypeVar)

	assert type_parameter.__name__ == ScalarValue.__name__
	assert type_parameter.__constraints__ == ScalarValue.__value__.__args__


@pytest.mark.parametrize("rejected_values", ["FR", [["FR"]]])
def test_is_in_rejects_a_text_or_values_that_are_not_single(rejected_values: object) -> None:
	"""
	Check that a single text, or a list holding a list, raises InvalidTypeError.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rejected_values
		A text, or a list of lists.
	"""
	untyped_is_in = cast(Any, IsIn)

	with pytest.raises(InvalidTypeError):
		untyped_is_in(rejected_values)

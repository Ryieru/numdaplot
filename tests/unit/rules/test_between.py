"""
Unit tests of Between.

.. versionadded:: 0.1.0
"""

from datetime import date, datetime
from typing import Any, TypeVar, cast

import pytest

from numdaplot.errors.invalid_bounds_error import InvalidBoundsError
from numdaplot.errors.invalid_setting_type_error import InvalidSettingTypeError
from numdaplot.rules.between import Between
from numdaplot.rules.bounds import Bounds
from numdaplot.rules.rule_values import OrderedValue

LOW_BOUND = 10
HIGH_BOUND = 20
DECIMAL_HIGH_BOUND = 20.5
FIRST_DAY = date(2026, 1, 1)
FIRST_DAY_AT_NOON = datetime(2026, 1, 1, 12)
TEXT_BOUND = "20"


def test_between_includes_both_bounds_by_default() -> None:
	"""
	Check that both bounds are included when bounds is omitted.

	.. versionadded:: 0.1.0
	"""
	rule = Between(low=LOW_BOUND, high=HIGH_BOUND)

	assert rule.bounds == Bounds.INCLUDED


def test_between_accepts_equal_bounds() -> None:
	"""
	Check that an interval reduced to a single value is accepted.

	.. versionadded:: 0.1.0
	"""
	rule = Between(low=LOW_BOUND, high=LOW_BOUND)

	assert rule.low == rule.high


def test_between_accepts_an_integer_and_a_decimal() -> None:
	"""
	Check that an integer and a decimal bound can be mixed.

	.. versionadded:: 0.1.0
	"""
	rule = Between(low=LOW_BOUND, high=DECIMAL_HIGH_BOUND)

	assert rule.high == DECIMAL_HIGH_BOUND


def test_between_rejects_reversed_bounds() -> None:
	"""
	Check that a low bound greater than the high bound is rejected.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidBoundsError):
		Between(low=HIGH_BOUND, high=LOW_BOUND)


def test_between_rejects_a_number_and_a_text() -> None:
	"""
	Check that bounds that Python cannot compare are rejected.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidBoundsError):
		Between[int | str](low=LOW_BOUND, high=TEXT_BOUND)  # pyright: ignore[reportInvalidTypeArguments]


def test_between_rejects_a_date_and_a_datetime() -> None:
	"""
	Check that a date and a datetime, which Python cannot compare, are rejected.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidBoundsError):
		Between(low=FIRST_DAY, high=FIRST_DAY_AT_NOON)


def test_between_type_parameter_holds_the_types_of_its_alias() -> None:
	"""
	Check that the type parameter shown as OrderedValue accepts exactly the types of this alias.

	.. versionadded:: 0.1.0
	"""
	type_parameter = Between.__type_params__[0]
	assert isinstance(type_parameter, TypeVar)

	assert type_parameter.__name__ == OrderedValue.__name__
	assert type_parameter.__constraints__ == OrderedValue.__value__.__args__


def test_between_rejects_a_bound_that_is_not_single() -> None:
	"""
	Check that None as a bound raises InvalidSettingTypeError.

	.. versionadded:: 0.1.0
	"""
	untyped_between = cast(Any, Between)

	with pytest.raises(InvalidSettingTypeError):
		untyped_between(low=None, high=HIGH_BOUND)

"""
Unit tests of ValueRule, the base of the single-value rules.

.. versionadded:: 0.1.0
"""

from dataclasses import FrozenInstanceError
from typing import Any, cast, get_type_hints

import pytest

from numdaplot.errors.invalid_setting_type_error import InvalidSettingTypeError
from numdaplot.errors.refused_operation_error import RefusedOperationError
from numdaplot.rules.equal import Equal
from numdaplot.rules.greater import Greater
from numdaplot.rules.greater_or_equal import GreaterOrEqual
from numdaplot.rules.less import Less
from numdaplot.rules.less_or_equal import LessOrEqual
from numdaplot.rules.not_equal import NotEqual
from numdaplot.rules.rule_values import OrderedValue, ScalarValue
from numdaplot.rules.value_rule import ValueRule, refuse_missing_value

REFERENCE_VALUE = 100
OTHER_VALUE = 200
VALUE_FIELD = "value"
EXPECTED_EQUAL_NONE_MESSAGE = "Equal(None) is not available, use IsMissing instead."
EXPECTED_NOT_EQUAL_NONE_MESSAGE = "NotEqual(None) is not available, use IsPresent instead."
LIST_VALUE = [1, 2]


def test_value_rule_keeps_its_reference_value() -> None:
	"""
	Check that the reference value is available as an attribute.

	.. versionadded:: 0.1.0
	"""
	rule = ValueRule(REFERENCE_VALUE)

	assert rule.value == REFERENCE_VALUE


def test_value_rule_cannot_be_modified() -> None:
	"""
	Check that the reference value cannot be replaced after creation.

	.. versionadded:: 0.1.0
	"""
	rule = ValueRule(REFERENCE_VALUE)

	with pytest.raises(FrozenInstanceError):
		setattr(rule, VALUE_FIELD, OTHER_VALUE)


def test_value_rules_of_different_classes_are_not_equal() -> None:
	"""
	Check that two rules with the same value but different classes are different.

	.. versionadded:: 0.1.0
	"""
	greater_rule = Greater(REFERENCE_VALUE)
	less_rule = Less(REFERENCE_VALUE)

	assert greater_rule != less_rule


def test_value_rules_of_the_same_class_and_value_are_equal() -> None:
	"""
	Check that two rules of the same class with the same value are equal.

	.. versionadded:: 0.1.0
	"""
	first_rule = Greater(REFERENCE_VALUE)
	second_rule = Greater(REFERENCE_VALUE)

	assert first_rule == second_rule


@pytest.mark.parametrize(
	("rule_class", "value_type"),
	[
		(Equal, ScalarValue),
		(NotEqual, ScalarValue),
		(Greater, OrderedValue),
		(GreaterOrEqual, OrderedValue),
		(Less, OrderedValue),
		(LessOrEqual, OrderedValue),
	],
)
def test_rule_declares_the_type_of_its_reference_value(rule_class: type, value_type: object) -> None:
	"""
	Check that each rule shows its own value type rather than the type parameter of its base.

	.. versionadded:: 0.1.0
	"""
	field_types = get_type_hints(rule_class)

	assert field_types["value"] is value_type


@pytest.mark.parametrize(
	("rule_class", "expected_message"),
	[(Equal, EXPECTED_EQUAL_NONE_MESSAGE), (NotEqual, EXPECTED_NOT_EQUAL_NONE_MESSAGE)],
)
def test_value_rule_points_none_to_the_rule_of_missing_values(rule_class: type[Any], expected_message: str) -> None:
	"""
	Check that Equal(None) and NotEqual(None) name the rule testing missing values.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rule_class
		Equal or NotEqual.
	expected_message
		The message naming IsMissing or IsPresent.
	"""
	with pytest.raises(RefusedOperationError) as error_info:
		rule_class(None)

	message = str(error_info.value)
	assert message == expected_message


@pytest.mark.parametrize("rejected_value", [None, LIST_VALUE])
def test_value_rule_rejects_a_value_that_is_not_single(rejected_value: object) -> None:
	"""
	Check that Greater refuses None and a list.

	.. versionadded:: 0.1.0

	Parameters
	----------
	rejected_value
		A value that is not a single value.
	"""
	untyped_greater = cast(Any, Greater)

	with pytest.raises(InvalidSettingTypeError):
		untyped_greater(rejected_value)


def test_refuse_missing_value_accepts_a_present_value() -> None:
	"""
	Check that a value that is not None passes.

	.. versionadded:: 0.1.0
	"""
	refuse_missing_value("Equal", "IsMissing", REFERENCE_VALUE)


def test_refuse_missing_value_accepts_none_without_a_rule_of_missing_values() -> None:
	"""
	Check that None passes when the rule has no rule of its own for missing values.

	.. versionadded:: 0.1.0
	"""
	refuse_missing_value("Greater", None, None)

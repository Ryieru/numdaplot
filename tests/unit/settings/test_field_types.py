"""
Unit tests of the check of the settings against their annotations.

.. versionadded:: 0.1.0
"""

from dataclasses import dataclass

import numpy
import pytest

from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.rules.rule_values import ScalarValue
from numdaplot.settings.annotation_kinds import (
	read_accepted_kinds,
)
from numdaplot.settings.field_types import accepts_value, find_field_checks, find_rejected_value, require_field_types

ACCEPTED_TEXTS = ["a", "b"]
EXPECTED_MESSAGE = "ProbeSetting count expects an int, got '2'."
ACCEPTED_CASES = [
	(int, 1, True),
	(int, numpy.int64(1), True),
	(int, True, False),
	(int, 1.5, False),
	(float, 1, True),
	(float, 1.5, True),
	(float, numpy.float64(1.5), True),
	(float, True, False),
	(bool, True, True),
	(bool, 1, False),
	(str, "a", True),
	(str, 1, False),
	(int | None, None, True),
	(list[str], ["a"], True),
	(list[str], ["a", 1], False),
	(list[str], ("a",), False),
	(ScalarValue, True, True),
	(ScalarValue, None, False),
]


@dataclass(frozen=True)
class ProbeSetting:
	"""
	A setting checked by the tests.

	.. versionadded:: 0.1.0

	Parameters
	----------
	count
		A number.
	"""

	count: int

	def __post_init__(self) -> None:
		"""
		Check the type of the count.

		.. versionadded:: 0.1.0

		Raises
		------
		InvalidTypeError
			When ``count`` is not an int.
		"""
		require_field_types(self)


@pytest.mark.parametrize(("annotation", "value", "expected"), ACCEPTED_CASES)
def test_accepts_value_follows_the_annotation(annotation: object, value: object, expected: bool) -> None:
	"""
	Check the numbers, the booleans, the lists and the aliases.

	.. versionadded:: 0.1.0

	Parameters
	----------
	annotation
		The annotation.
	value
		The value.
	expected
		Whether the annotation accepts it.
	"""
	kinds = read_accepted_kinds(annotation)

	is_accepted = accepts_value(kinds, value)

	assert is_accepted == expected


def test_require_field_types_names_the_field_and_its_type() -> None:
	"""
	Check the message of a field holding another type.

	.. versionadded:: 0.1.0
	"""
	with pytest.raises(InvalidTypeError) as error_info:
		ProbeSetting(count="2")  # pyright: ignore[reportArgumentType]

	message = str(error_info.value)
	assert message == EXPECTED_MESSAGE


def test_find_field_checks_builds_the_checks_once() -> None:
	"""
	Check that a class gets the same checks at each call.

	.. versionadded:: 0.1.0
	"""
	first_checks = find_field_checks(ProbeSetting)
	second_checks = find_field_checks(ProbeSetting)

	assert first_checks is second_checks


def test_find_rejected_value_gives_the_first_rejected_item() -> None:
	"""
	Check that a list points to its rejected item.

	.. versionadded:: 0.1.0
	"""
	kinds = read_accepted_kinds(list[str])

	rejected_value = find_rejected_value(kinds, ["a", 1, 2])

	assert rejected_value == 1


def test_find_rejected_value_gives_the_whole_list_when_every_item_is_accepted() -> None:
	"""
	Check that a list without rejected item is itself the rejected value.

	.. versionadded:: 0.1.0
	"""
	kinds = read_accepted_kinds(list[str])

	rejected_value = find_rejected_value(kinds, ACCEPTED_TEXTS)

	assert rejected_value == ACCEPTED_TEXTS

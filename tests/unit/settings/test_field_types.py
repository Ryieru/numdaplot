"""
Unit tests of the check of the settings against their annotations.

.. versionadded:: 0.1.0
"""

import typing
from dataclasses import dataclass

import numpy
import pytest

import numdaplot as ndp
from numdaplot.errors.invalid_type_error import InvalidTypeError
from numdaplot.rules.rule_values import ScalarValue
from numdaplot.settings.field_types import (
	accepts_value,
	add_article,
	describe_kinds,
	find_field_checks,
	find_member_classes,
	find_member_name,
	find_rejected_value,
	join_names,
	list_annotation_members,
	read_accepted_kinds,
	read_annotations,
	require_field_types,
)

EXPECTED_SINGLE_MEMBERS = [int, type(None)]
ACCEPTED_TEXTS = ["a", "b"]
EXPECTED_MESSAGE = "ProbeSetting count expects an int, got '2'."
type TextPairs[ItemType] = list[ItemType]
CLASS_MESSAGE = "ndp.Mean is a class, use ndp.Mean() instead."
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


def test_read_annotations_resolves_the_names_only_known_to_the_type_checker() -> None:
	"""
	Check that the texts naming Array and Table become the classes.

	.. versionadded:: 0.1.0
	"""
	annotations = read_annotations(ndp.Equality)

	assert annotations["other"] == ndp.Array | ndp.Table


def test_list_annotation_members_expands_a_union() -> None:
	"""
	Check the members of a union.

	.. versionadded:: 0.1.0
	"""
	members = list_annotation_members(int | None)

	assert members == EXPECTED_SINGLE_MEMBERS


def test_find_member_classes_accepts_numpy_numbers_for_a_float() -> None:
	"""
	Check the classes accepted for a float.

	.. versionadded:: 0.1.0
	"""
	classes = find_member_classes(float)

	assert numpy.floating in classes
	assert numpy.integer in classes


def test_find_member_name_writes_none() -> None:
	"""
	Check the name of the type of None.

	.. versionadded:: 0.1.0
	"""
	member_name = find_member_name(type(None))

	assert member_name == "None"


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


def test_list_annotation_members_expands_a_generic_type_alias() -> None:
	"""
	Check that a type alias with a parameter is read as the type it names.

	.. versionadded:: 0.1.0
	"""
	members = list_annotation_members(TextPairs[str])

	member_origins = [typing.get_origin(member) for member in members]
	assert member_origins == [list]


def test_describe_kinds_shows_a_text_inside_a_list() -> None:
	"""
	Check the description for a text given in place of a list.

	.. versionadded:: 0.1.0
	"""
	kinds = read_accepted_kinds(list[str])

	description = describe_kinds(kinds, "price")

	assert description == "a list such as ['price']"


def test_describe_kinds_lists_every_kind() -> None:
	"""
	Check the description of a union with a list.

	.. versionadded:: 0.1.0
	"""
	kinds = read_accepted_kinds(int | list[str] | None)

	description = describe_kinds(kinds, 1.5)

	assert description == "an int, None or a list of str"


def test_add_article_chooses_a_or_an() -> None:
	"""
	Check both articles.

	.. versionadded:: 0.1.0
	"""
	assert add_article("Index") == "an Index"
	assert add_article("Range") == "a Range"
	assert add_article("Uniform") == "a Uniform"


def test_join_names_keeps_a_single_name() -> None:
	"""
	Check that a single name stays as it is.

	.. versionadded:: 0.1.0
	"""
	joined_names = join_names(["an int"])

	assert joined_names == "an int"

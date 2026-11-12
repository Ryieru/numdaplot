"""
Unit tests of the reading of an annotation as the values a setting accepts.

.. versionadded:: 0.2.0
"""

import typing

import numpy

import numdaplot as ndp
from numdaplot.settings.annotation_kinds import (
	find_member_classes,
	find_member_name,
	list_annotation_members,
	read_annotations,
)

type TextPairs[ItemType] = list[ItemType]

EXPECTED_SINGLE_MEMBERS = [int, type(None)]


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


def test_list_annotation_members_expands_a_generic_type_alias() -> None:
	"""
	Check that a type alias with a parameter is read as the type it names.

	.. versionadded:: 0.1.0
	"""
	members = list_annotation_members(TextPairs[str])

	member_origins = [typing.get_origin(member) for member in members]
	assert member_origins == [list]

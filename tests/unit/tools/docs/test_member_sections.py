"""
Unit tests of the sections of the members of the Array, Table and Plot pages.

.. versionadded:: 0.2.0
"""

from dataclasses import dataclass

import pytest
from member_sections import (
	MemberSection,
	find_member_sections,
	find_part_members,
	is_documented_member,
	list_documented_members,
	read_source_member_names,
)

import numdaplot as ndp

LAYOUT_TITLE = "Layout"
EXPECTED_SELECTION_MEMBERS = ("pick", "size", "build", "__repr__")
EXPECTED_LAYOUT_MEMBERS = ("flip",)
SELECTION_SECTION = MemberSection("Selection", EXPECTED_SELECTION_MEMBERS)
LAYOUT_SECTION = MemberSection(LAYOUT_TITLE, EXPECTED_LAYOUT_MEMBERS)
EXPECTED_SHAPE_SECTIONS = [SELECTION_SECTION, LAYOUT_SECTION]
EXPECTED_PART_MEMBERS = {"Selection": EXPECTED_SELECTION_MEMBERS, "Layout": EXPECTED_LAYOUT_MEMBERS}
DOCUMENTED_CLASSES = [ndp.Array, ndp.Table, ndp.Plot]
SPECIAL_NAME = "__add__"
PRIVATE_NAME = "_wrap"
INIT_NAME = "__init__"
PUBLIC_NAME = "pick"
PRIVATE_MARK = "_"
EXPECTED_RECORD_MEMBERS = ("keep",)
EXPECTED_LAYOUT_SOURCE_NAMES = frozenset(EXPECTED_LAYOUT_MEMBERS)


class ShapeData:
	"""
	Fake base holding no documented member.

	.. versionadded:: 0.2.0
	"""

	stored_value = 0

	def _wrap(self) -> None:
		"""
		Fake private helper.

		.. versionadded:: 0.2.0
		"""


class ShapeLayout(ShapeData):
	"""
	Fake part class with one method.

	.. versionadded:: 0.2.0
	"""

	def flip(self) -> None:
		"""
		Fake method.

		.. versionadded:: 0.2.0
		"""


class ShapeSelection(ShapeData):
	"""
	Fake part class with every kind of member, in a known order.

	.. versionadded:: 0.2.0
	"""

	marker = None

	def __init__(self) -> None:
		"""
		Fake creation, hidden from the documentation.

		.. versionadded:: 0.2.0
		"""

	def pick(self) -> None:
		"""
		Fake method.

		.. versionadded:: 0.2.0
		"""

	@property
	def size(self) -> int:
		"""
		Fake attribute.

		.. versionadded:: 0.2.0

		Returns
		-------
		int
			Always 0.
		"""
		return 0

	@classmethod
	def build(cls) -> None:
		"""
		Fake creation method.

		.. versionadded:: 0.2.0
		"""

	def _check(self) -> None:
		"""
		Fake private helper.

		.. versionadded:: 0.2.0
		"""

	def __repr__(self) -> str:
		"""
		Fake text.

		.. versionadded:: 0.2.0

		Returns
		-------
		str
			Always empty.
		"""
		return ""


@dataclass
class ShapeRecord:
	"""
	Fake part class whose ``__init__``, ``__repr__`` and ``__eq__`` are added at run time by ``dataclass``.

	.. versionadded:: 0.2.0
	"""

	def keep(self) -> None:
		"""
		Fake method.

		.. versionadded:: 0.2.0
		"""


class Shape(ShapeSelection, ShapeLayout):
	"""
	Fake class built from part classes named after it.

	.. versionadded:: 0.2.0
	"""


class ShapeMystery(ShapeData):
	"""
	Fake part class whose end of name has no title.

	.. versionadded:: 0.2.0
	"""

	def guess(self) -> None:
		"""
		Fake method.

		.. versionadded:: 0.2.0
		"""


class OddShape(ShapeMystery):
	"""
	Fake class whose bases are not named after it.

	.. versionadded:: 0.2.0
	"""


class MysteryTrick(ShapeData):
	"""
	Fake part class with one method and an end of name missing from the titles.

	.. versionadded:: 0.2.0
	"""

	def trick(self) -> None:
		"""
		Fake method.

		.. versionadded:: 0.2.0
		"""


class Mystery(MysteryTrick):
	"""
	Fake class built from a part class whose end of name has no title.

	.. versionadded:: 0.2.0
	"""


def test_find_member_sections_follows_the_order_of_the_titles() -> None:
	"""
	Check that Selection comes before Layout, as in the titles, whatever the order of the bases.

	.. versionadded:: 0.2.0
	"""
	member_sections = find_member_sections(Shape)

	assert member_sections == EXPECTED_SHAPE_SECTIONS


def test_find_member_sections_gives_none_for_a_class_without_parts() -> None:
	"""
	Check that a class whose bases are not named after it has no section.

	.. versionadded:: 0.2.0
	"""
	member_sections = find_member_sections(OddShape)

	assert member_sections == []


def test_find_member_sections_rejects_an_end_of_name_without_title() -> None:
	"""
	Check that a part class missing from the titles raises KeyError.

	.. versionadded:: 0.2.0
	"""
	with pytest.raises(KeyError):
		find_member_sections(Mystery)


def test_find_member_sections_gives_the_same_title_to_the_same_end_of_name() -> None:
	"""
	Check that ArrayLayout and TableLayout both give a Layout section.

	.. versionadded:: 0.2.0
	"""
	array_sections = find_member_sections(ndp.Array)
	table_sections = find_member_sections(ndp.Table)

	array_titles = [member_section.title for member_section in array_sections]
	table_titles = [member_section.title for member_section in table_sections]
	assert LAYOUT_TITLE in array_titles
	assert LAYOUT_TITLE in table_titles


@pytest.mark.parametrize("documented_class", DOCUMENTED_CLASSES)
def test_find_member_sections_lists_every_public_member(documented_class: type) -> None:
	"""
	Check that every public method and attribute of Array, Table and Plot appears in a section.

	.. versionadded:: 0.2.0

	Parameters
	----------
	documented_class
		``Array``, ``Table`` or ``Plot``.
	"""
	member_sections = find_member_sections(documented_class)
	listed_names = {member_name for member_section in member_sections for member_name in member_section.member_names}
	every_name = dir(documented_class)
	public_names = {member_name for member_name in every_name if not member_name.startswith(PRIVATE_MARK)}
	missing_names = public_names - listed_names
	assert missing_names == set()


def test_find_part_members_skips_the_parts_without_documented_member() -> None:
	"""
	Check that ShapeData, holding only a value and a private helper, gives no entry.

	.. versionadded:: 0.2.0
	"""
	part_members = find_part_members(Shape)

	assert part_members == EXPECTED_PART_MEMBERS


def test_list_documented_members_keeps_the_order_of_the_code() -> None:
	"""
	Check the methods, attribute and special method kept, without values, private helpers and ``__init__``.

	.. versionadded:: 0.2.0
	"""
	member_names = list_documented_members(ShapeSelection)

	assert member_names == EXPECTED_SELECTION_MEMBERS


def test_list_documented_members_leaves_out_the_members_added_at_run_time() -> None:
	"""
	Check that the ``__repr__`` and ``__eq__`` made by ``dataclass``, missing from the source, are hidden.

	.. versionadded:: 0.2.0
	"""
	member_names = list_documented_members(ShapeRecord)

	assert member_names == EXPECTED_RECORD_MEMBERS


def test_read_source_member_names_gives_the_members_of_the_class_body() -> None:
	"""
	Check that only the method written in ShapeLayout is read, without the members of its base.

	.. versionadded:: 0.2.0
	"""
	source_names = read_source_member_names(ShapeLayout)

	assert source_names == EXPECTED_LAYOUT_SOURCE_NAMES


def test_is_documented_member_keeps_a_special_method() -> None:
	"""
	Check that an operator such as ``__add__`` is shown.

	.. versionadded:: 0.2.0
	"""
	is_documented = is_documented_member(SPECIAL_NAME, ShapeSelection.__repr__)

	assert is_documented


def test_is_documented_member_hides_a_private_helper() -> None:
	"""
	Check that a name starting with one underscore is hidden.

	.. versionadded:: 0.2.0
	"""
	is_documented = is_documented_member(PRIVATE_NAME, ShapeData._wrap)  # pyright: ignore[reportPrivateUsage]

	assert not is_documented


def test_is_documented_member_hides_the_creation() -> None:
	"""
	Check that ``__init__`` is hidden.

	.. versionadded:: 0.2.0
	"""
	is_documented = is_documented_member(INIT_NAME, ShapeSelection.__init__)

	assert not is_documented


def test_is_documented_member_hides_a_plain_value() -> None:
	"""
	Check that a public name holding a value, not a method, is hidden.

	.. versionadded:: 0.2.0
	"""
	is_documented = is_documented_member(PUBLIC_NAME, None)

	assert not is_documented

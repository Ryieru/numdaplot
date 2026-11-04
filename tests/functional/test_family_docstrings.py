"""
Functional tests checking that the docstring of each base class lists every exported member of its family.

.. versionadded:: 0.1.0
"""

import inspect

import pytest

import numdaplot as ndp

FAMILY_BASES = [ndp.Rule, ndp.Statistic, ndp.MathFunction, ndp.Distribution, ndp.TimeFunction, ndp.Chart]
MEMBER_ROW = "| ``{name}`` |"
LISTING_DOCSTRING = "| ``LessOrEqual`` | The values less than or equal to a value | ``ndp.LessOrEqual(10)`` |"
LISTED_MEMBER = "LessOrEqual"
UNLISTED_MEMBER = "Less"


def find_exported_members(base: type) -> list[str]:
	"""
	Return the names exported by numdaplot that are subclasses of a base class.

	.. versionadded:: 0.1.0

	Parameters
	----------
	base
		The base class of a family.

	Returns
	-------
	list[str]
		The name of each exported subclass, without the base class itself.
	"""
	member_names = list[str]()

	for name in ndp.__all__:
		exported_object = getattr(ndp, name)
		if not inspect.isclass(exported_object):
			continue

		is_subclass = issubclass(exported_object, base)
		if is_subclass and exported_object is not base:
			member_names.append(name)

	return member_names


def find_unlisted_members(docstring: str, member_names: list[str]) -> list[str]:
	"""
	Return the names that have no row of their own in the table of a docstring.

	.. versionadded:: 0.1.0

	Parameters
	----------
	docstring
		The docstring holding the table.
	member_names
		The names expected in the first column of the table.

	Returns
	-------
	list[str]
		The names without a row, in the order given.
	"""
	unlisted_names = list[str]()

	for name in member_names:
		member_row = MEMBER_ROW.format(name=name)
		if member_row not in docstring:
			unlisted_names.append(name)

	return unlisted_names


@pytest.mark.parametrize("base", FAMILY_BASES)
def test_family_has_exported_members(base: type) -> None:
	"""A family exports at least one member."""
	member_names = find_exported_members(base)

	assert member_names


@pytest.mark.parametrize("base", FAMILY_BASES)
def test_base_docstring_lists_every_exported_member(base: type) -> None:
	"""The table of a base class has one row for each exported member."""
	member_names = find_exported_members(base)
	docstring = inspect.getdoc(base)
	assert docstring is not None

	unlisted_names = find_unlisted_members(docstring, member_names)

	assert unlisted_names == []


def test_find_unlisted_members_keeps_a_name_that_is_only_part_of_another() -> None:
	"""A name found only inside a longer name has no row of its own."""
	member_names = [LISTED_MEMBER, UNLISTED_MEMBER]

	unlisted_names = find_unlisted_members(LISTING_DOCSTRING, member_names)

	assert unlisted_names == [UNLISTED_MEMBER]

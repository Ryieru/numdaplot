"""
Unit tests of the description of what a setting accepts.

.. versionadded:: 0.2.0
"""

from numdaplot.argument_checks.annotation_kinds import (
	read_accepted_kinds,
)
from numdaplot.argument_checks.kind_descriptions import add_article, describe_kinds, join_names


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

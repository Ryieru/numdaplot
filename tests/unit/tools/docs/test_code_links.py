"""
Unit tests of the links of the names of a text written in code.

.. versionadded:: 0.1.0
"""

import griffe
from code_links import escape_code, find_instance_member, find_keyword_identifier, link_code_tokens
from link_targets import LinkContext, find_public_paths

PACKAGE_NAME = "sales"
PACKAGE_FILES = {
	"__init__.py": "from sales.table import Table\nfrom sales.uniform import Uniform\n",
	"uniform.py": "class Uniform:\n    low: float\n    high: float\n",
	"table.py": "class Table:\n    INT64 = 1\n    low: float\n    def to_csv(self) -> None: ...\n",
}
TABLE_PATH = "sales.table.Table"
UNIFORM_PATH = "sales.uniform.Uniform"
LOW_PATH = "sales.uniform.Uniform.low"
TO_CSV_PATH = "sales.table.Table.to_csv"
INT64_PATH = "sales.table.Table.INT64"
ENUM_MEMBER_PATHS = {"INT64": INT64_PATH}
UNIFORM_LINK = (
	'<span class="api-link api-link-class"><autoref identifier="sales.uniform.Uniform" optional>ndp.Uniform'
	"</autoref></span>"
)
LOW_LINK = (
	'<span class="api-link api-link-attribute"><autoref identifier="sales.uniform.Uniform.low" optional>low'
	"</autoref></span>"
)
INT64_LINK = (
	'<span class="api-link api-link-attribute"><autoref identifier="sales.table.Table.INT64" optional>INT64'
	"</autoref></span>"
)
TABLE_LINK_START = '<span class="api-link api-link-class"><autoref identifier="sales.table.Table" optional>'
LIBRARY_NAME = "pandas.to_csv"
INSTANCE_CALL = "table.to_csv()"
UNKNOWN_MEMBER = "table.to_json"
TO_CSV_LINK_START = '<autoref identifier="sales.table.Table.to_csv" optional>'
PLAIN_CODE = "1 + 2"
SPECIAL_TEXT = "[a_b] * <c>"
ESCAPED_SPECIAL_TEXT = "&#91;a&#95;b&#93; &#42; &lt;c&gt;"


def build_context(class_path: str | None) -> LinkContext:
	"""
	Return the link context of a docstring of a small package.

	.. versionadded:: 0.1.0

	Parameters
	----------
	class_path
		The documented class owning the docstring.

	Returns
	-------
	LinkContext
		The context.
	"""
	loader = griffe.GriffeLoader()
	with griffe.temporary_visited_package(PACKAGE_NAME, PACKAGE_FILES) as package:
		loader.modules_collection.set_member(package.path, package)
		loader.resolve_aliases()

	public_paths = find_public_paths(package)
	context = LinkContext(class_path, public_paths, loader, ENUM_MEMBER_PATHS)

	return context


def test_link_code_tokens_links_a_class_called_with_arguments() -> None:
	"""
	Check that the class is a link and its arguments stay next to it.

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	links = link_code_tokens("ndp.Uniform(1, 2)", context)

	assert links == UNIFORM_LINK + "(1, 2)"


def test_link_code_tokens_links_each_name_of_a_list() -> None:
	"""
	Check two calls inside a list, whose brackets stay out of the reach of Markdown.

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	links = link_code_tokens("[ndp.Uniform(1), ndp.Uniform(2)]", context)

	assert links == "&#91;" + UNIFORM_LINK + "(1), " + UNIFORM_LINK + "(2)&#93;"


def test_link_code_tokens_links_a_keyword_to_the_attribute_of_the_called_class() -> None:
	"""
	Check that low links to Uniform.low.

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	links = link_code_tokens("ndp.Uniform(low=1)", context)

	assert links == UNIFORM_LINK + "(" + LOW_LINK + "=1)"


def test_link_code_tokens_reads_a_keyword_after_inner_parentheses() -> None:
	"""
	Check that closing inner parentheses goes back to the call around them.

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	links = link_code_tokens("ndp.Uniform((1), low=1)", context)

	assert links == UNIFORM_LINK + "((1), " + LOW_LINK + "=1)"


def test_link_code_tokens_keeps_a_keyword_the_called_class_does_not_have() -> None:
	"""
	Check that seed stays plain text.

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	links = link_code_tokens("ndp.Uniform(seed=1)", context)

	assert links == UNIFORM_LINK + "(seed=1)"


def test_link_code_tokens_does_not_read_a_keyword_on_the_documented_class() -> None:
	"""
	Check that a keyword of an unknown call stays plain, though the documented class has this attribute.

	.. versionadded:: 0.1.0
	"""
	context = build_context(TABLE_PATH)

	links = link_code_tokens("load(low=1)", context)

	assert links is None


def test_link_code_tokens_keeps_the_quoted_texts() -> None:
	"""
	Check that a public name inside quotes is no link.

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	links = link_code_tokens('ndp.Uniform("Table")', context)

	assert links == UNIFORM_LINK + '("Table")'


def test_link_code_tokens_links_a_public_name_inside_a_text() -> None:
	"""
	Check the class of a code such as "a Table".

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	links = link_code_tokens("a Table", context)

	assert links is not None
	assert TABLE_LINK_START in links


def test_link_code_tokens_links_an_enum_member_alone() -> None:
	"""
	Check that INT64 links to the only class holding it.

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	links = link_code_tokens("INT64", context)

	assert links == INT64_LINK


def test_link_code_tokens_gives_nothing_without_a_known_name() -> None:
	"""
	Check code holding no name of the package.

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	links = link_code_tokens(PLAIN_CODE, context)

	assert links is None


def test_find_keyword_identifier_finds_the_attribute_of_the_call() -> None:
	"""
	Check that low is found on Uniform.

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	identifier = find_keyword_identifier("low", UNIFORM_PATH, context.loader)

	assert identifier == LOW_PATH


def test_find_keyword_identifier_gives_nothing_for_an_unknown_call() -> None:
	"""
	Check a keyword given to a call that matches no object.

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	identifier = find_keyword_identifier("low", None, context.loader)

	assert identifier is None


def test_find_instance_member_reads_a_member_on_an_instance_of_the_documented_class() -> None:
	"""
	Check that table.to_csv links to Table.to_csv in the documentation of Table.

	.. versionadded:: 0.1.0
	"""
	context = build_context(TABLE_PATH)

	identifier = find_instance_member("table.to_csv", context)

	assert identifier == TO_CSV_PATH


def test_find_instance_member_leaves_the_names_of_a_library() -> None:
	"""
	Check that a function of another library is not taken for a member of the documented class.

	.. versionadded:: 0.1.0
	"""
	context = build_context(TABLE_PATH)

	identifier = find_instance_member(LIBRARY_NAME, context)

	assert identifier is None


def test_find_instance_member_gives_nothing_outside_a_class() -> None:
	"""
	Check a docstring that no class owns.

	.. versionadded:: 0.1.0
	"""
	context = build_context(None)

	identifier = find_instance_member("table.to_csv", context)

	assert identifier is None


def test_escape_code_writes_html_and_markdown_characters_as_entities() -> None:
	"""
	Check brackets, underscore, star and angle brackets.

	.. versionadded:: 0.1.0
	"""
	escaped_text = escape_code(SPECIAL_TEXT)

	assert escaped_text == ESCAPED_SPECIAL_TEXT


def test_find_instance_member_gives_nothing_for_a_member_the_class_does_not_have() -> None:
	"""
	Check that a name written on the instance but missing from the documented class is not linked.

	.. versionadded:: 0.1.0
	"""
	context = build_context(TABLE_PATH)

	identifier = find_instance_member(UNKNOWN_MEMBER, context)

	assert identifier is None


def test_link_code_tokens_links_a_member_called_on_an_instance() -> None:
	"""
	Check that table.to_csv() in the documentation of Table links to Table.to_csv.

	.. versionadded:: 0.1.0
	"""
	context = build_context(TABLE_PATH)

	links = link_code_tokens(INSTANCE_CALL, context)

	assert links is not None
	assert TO_CSV_LINK_START in links
